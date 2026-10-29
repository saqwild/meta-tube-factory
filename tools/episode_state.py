"""Episode state machine. Plain JSON + a plain-text log. No git.

This module is the only place that reads/writes episode-state.json, so the
state file's shape stays consistent regardless of which command touched it.

Durability (no git, so this is the whole chain of custody):
  * every state write is atomic -- a temp file + os.replace, never a partial file;
  * the previous state is kept as episode-state.json.bak before each write, so a
    torn or bad write is recoverable;
  * a stage-advancing operation (complete/reopen) takes a per-episode lock file
    so two operators cannot both read-advance-write the same episode and lose one
    of the completions;
  * within the lock the order is bak -> log-append -> atomic state write, so a
    crash mid-operation leaves the state consistent (at worst an orphan log line
    for a completion that did not take effect, which is self-explanatory).
"""
import contextlib
import hashlib
import json
import os
import re
import time
from datetime import datetime, timezone
from pathlib import Path

from project_paths import CHANNEL_PROFILES_DIR, EPISODES_DIR, STAGES_DIR


class PipelineError(Exception):
    pass


# A lock older than this is treated as abandoned (a crashed operator) and broken
# automatically. State operations here are sub-second; an hour is unambiguous.
_LOCK_STALE_SECONDS = 3600

# The state machine's own files. They are 00-preflight's declared gate outputs but
# are not deliverables an approval is taken against -- excluded from digests.
_STATE_MACHINE_FILES = frozenset({
    "episode-state.json", "episode-state.json.bak", "episode-state.json.tmp",
    "episode-state.lock", "episode-state-log.md",
})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _atomic_write(path: Path, text: str) -> None:
    """Write via a temp file in the same directory + os.replace (atomic on one
    filesystem, on both POSIX and Windows). The reader never sees a partial file."""
    tmp = path.with_name(f"{path.name}.tmp.{os.getpid()}")
    tmp.write_text(text, encoding="utf-8")
    try:
        os.replace(tmp, path)
    except OSError:
        with contextlib.suppress(OSError):
            tmp.unlink()
        raise


def _append_line(path: Path, line: str) -> None:
    """Append one line in a single O_APPEND write -- as close to atomic as a plain
    text log gets; concurrent appends interleave by line, not mid-line."""
    with path.open("a", encoding="utf-8") as f:
        f.write(line if line.endswith("\n") else line + "\n")
        f.flush()
        with contextlib.suppress(OSError, AttributeError):
            os.fsync(f.fileno())


@contextlib.contextmanager
def _episode_lock(slug: str, episode_id: str):
    """Serialize stage-advancing operations on one episode. Raises if another
    operator holds a fresh lock; breaks a lock older than _LOCK_STALE_SECONDS."""
    lock = _episode_dir(slug, episode_id) / "episode-state.lock"
    if lock.exists():
        try:
            age = time.time() - lock.stat().st_mtime
            holder = lock.read_text(encoding="utf-8").strip()
        except OSError:
            age, holder = 0.0, "?"
        if age < _LOCK_STALE_SECONDS:
            raise PipelineError(
                f"{episode_id}: another operator holds the state lock "
                f"({holder}, {int(age)}s old). Wait, or if it is stale delete "
                f"{lock}."
            )
        with contextlib.suppress(OSError):
            lock.unlink()  # abandoned
    try:
        fd = os.open(str(lock), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
    except FileExistsError:
        raise PipelineError(
            f"{episode_id}: lost a race for the state lock; another operator is "
            f"mid-operation. Retry in a moment."
        )
    try:
        os.write(fd, f"pid {os.getpid()} @ {_now()}".encode())
        os.close(fd)
        yield
    finally:
        with contextlib.suppress(OSError):
            lock.unlink()


def list_channel_slugs() -> list[str]:
    return sorted(
        p.name for p in CHANNEL_PROFILES_DIR.iterdir()
        if p.is_dir() and (p / "channel.json").exists()
    )


def load_channel(slug: str) -> dict:
    path = CHANNEL_PROFILES_DIR / slug / "channel.json"
    if not path.exists():
        raise PipelineError(f"No channel profile at {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("slug") != slug:
        raise PipelineError(
            f"{path} declares slug={data.get('slug')!r}, expected {slug!r}"
        )
    stages = [s["id"] for s in data["pipeline_stages"]]
    missing = [s for s in stages if not (STAGES_DIR / f"{s}.md").exists()]
    if missing:
        raise PipelineError(
            f"{slug}: pipeline_stages reference missing contract file(s): {missing}"
        )
    return data


def preflight_check() -> list[str]:
    """Validate every declared channel profile. Returns the list of valid slugs."""
    if not CHANNEL_PROFILES_DIR.exists():
        raise PipelineError(f"Missing {CHANNEL_PROFILES_DIR}")
    slugs = list_channel_slugs()
    if not slugs:
        raise PipelineError(f"No channel profiles found under {CHANNEL_PROFILES_DIR}")
    for slug in slugs:
        load_channel(slug)  # raises on any structural problem
    return slugs


def _episode_dir(slug: str, episode_id: str) -> Path:
    return EPISODES_DIR / slug / episode_id


def list_episodes(slug: str) -> list[dict]:
    base = EPISODES_DIR / slug
    if not base.exists():
        return []
    out = []
    for d in sorted(base.iterdir()):
        state_path = d / "episode-state.json"
        if state_path.exists():
            state = json.loads(state_path.read_text(encoding="utf-8"))
            out.append(state)
    return out


def next_episode_id(slug: str) -> str:
    existing = list_episodes(slug)
    numbers = []
    for ep in existing:
        m = re.match(r"^EP(\d{3})", ep["episode_id"])
        if m:
            numbers.append(int(m.group(1)))
    n = (max(numbers) + 1) if numbers else 1
    return f"EP{n:03d}"


def _append_log(slug: str, episode_id: str, line: str) -> None:
    _append_line(
        _episode_dir(slug, episode_id) / "episode-state-log.md",
        f"- {_now()} -- {line}",
    )


def create_episode(slug: str) -> dict:
    channel = load_channel(slug)
    episode_id = next_episode_id(slug)
    stage_sequence = [s["id"] for s in channel["pipeline_stages"]]
    ep_dir = _episode_dir(slug, episode_id)
    try:
        ep_dir.mkdir(parents=True, exist_ok=False)  # also the create-race guard
    except FileExistsError:
        raise PipelineError(
            f"{slug}/{episode_id} already exists -- another operator just created it. "
            f"Re-run to get the next free id."
        )
    now = _now()
    state = {
        "episode_id": episode_id,
        "channel_slug": slug,
        "status": "open",
        "stage_sequence": stage_sequence,
        "next_stage": stage_sequence[0],
        "completed_stages": [],
        "created_at": now,
        "updated_at": now,
    }
    _atomic_write(
        ep_dir / "episode-state.json", json.dumps(state, indent=2) + "\n"
    )
    (ep_dir / "episode-state-log.md").write_text(
        f"# {episode_id} ({slug}) -- state log\n\n"
        f"- {now} -- episode created, channel={channel['channel']['name']!r}, "
        f"stage_sequence={stage_sequence}\n",
        encoding="utf-8",
    )
    return state


def load_state(slug: str, episode_id: str) -> dict:
    path = _episode_dir(slug, episode_id) / "episode-state.json"
    if not path.exists():
        raise PipelineError(f"No episode-state.json at {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        bak = path.with_name(path.name + ".bak")
        hint = (
            f" A pre-write backup exists at {bak} -- inspect it and, if it is the "
            f"last good state, copy it over {path.name}."
            if bak.exists() else ""
        )
        raise PipelineError(f"{path} is corrupt ({exc}).{hint}") from exc


def _save_state(slug: str, episode_id: str, state: dict) -> None:
    state["updated_at"] = _now()
    path = _episode_dir(slug, episode_id) / "episode-state.json"
    if path.exists():
        try:
            current = path.read_text(encoding="utf-8")
            json.loads(current)  # only keep a backup of a file that parses
            _atomic_write(path.with_name(path.name + ".bak"), current)
        except (OSError, json.JSONDecodeError):
            pass
    _atomic_write(path, json.dumps(state, indent=2) + "\n")


def stage_owner_gate(slug: str, stage_id: str) -> bool:
    channel = load_channel(slug)
    for s in channel["pipeline_stages"]:
        if s["id"] == stage_id:
            return bool(s.get("owner_gate", False))
    raise PipelineError(f"{slug} has no stage {stage_id!r} in pipeline_stages")


_STAGE_GATES_PATH = STAGES_DIR.parent / "stage-gates.json"


def _load_stage_gates() -> dict:
    if not _STAGE_GATES_PATH.exists():
        return {}
    data = json.loads(_STAGE_GATES_PATH.read_text(encoding="utf-8"))
    return {k: v for k, v in data.items() if not k.startswith("_")}  # "_..." keys are comments


def stage_spec(gates: dict, stage_id: str, stage_sequence) -> dict:
    """The effective gate for a stage in one episode: its base entry plus any
    `when_stage` extras whose key stage is in that episode's own sequence.

    `when_stage` lets a gate tighten only for episodes that run a given stage --
    e.g. inside-the-process episodes created after 01b-coverage-scan existed get
    coverage checks at 02/02a/03a/03b, while older episodes (whose frozen
    sequence has no 01b) and other channels are untouched. Returns
    {"outputs": [...], "verdicts": [...], "forbid": [...]}."""
    base = gates.get(stage_id) or {}
    spec = {
        "outputs": list(base.get("outputs", [])),
        "verdicts": [base["verdict"]] if base.get("verdict") else [],
        "forbid": list(base.get("forbid", [])),
    }
    for needed, extra in (base.get("when_stage") or {}).items():
        if needed in (stage_sequence or []):
            spec["outputs"] += [o for o in extra.get("outputs", []) if o not in spec["outputs"]]
            if extra.get("verdict"):
                spec["verdicts"].append(extra["verdict"])
            spec["forbid"] += extra.get("forbid", [])
    return spec


def stage_gate_check(slug: str, episode_id: str, stage_id: str) -> None:
    """Raise PipelineError unless the stage's declared deliverables exist and its
    verdict artifact (if any) carries a passing, non-blocking result.

    Sequence order and the owner-approval flag are checked by the caller; this is
    the separate check that the stage actually *produced* what it was supposed to,
    and that a BLOCKED / REVISE / non-PASS verdict stops the pipeline rather than
    riding through on the approval flag. Stages with no entry in stage-gates.json
    are a no-op here.
    """
    gates = _load_stage_gates()
    if stage_id not in gates:
        return
    spec = stage_spec(gates, stage_id, load_state(slug, episode_id).get("stage_sequence"))
    ep = _episode_dir(slug, episode_id)
    problems: list[str] = []

    for pat in spec.get("outputs", []):
        if any(ch in pat for ch in "*?["):
            if not list(ep.glob(pat)):
                problems.append(f"no file matches required output {pat!r}")
        else:
            p = ep / pat
            if not p.exists():
                problems.append(f"required output missing: {pat}")
            elif p.is_file() and p.stat().st_size == 0:
                problems.append(f"required output is empty: {pat}")

    # A marker that must be gone before the stage counts as done -- e.g. 04f's
    # "PROVISIONAL" header on 7-video-prompts.md, which only the 04f3 re-anchor
    # pass removes. Without this, 04f3 could complete on untouched draft prose.
    for rule in spec.get("forbid", []):
        fp = ep / rule["file"]
        if fp.is_file() and re.search(rule["pattern"], fp.read_text(encoding="utf-8")):
            problems.append(f"{rule['file']} still matches /{rule['pattern']}/ -- "
                            f"{rule.get('reason', 'this marker must be removed first')}")

    for verdict in spec["verdicts"]:
        if not problems:
            problems += _verdict_problems(ep, verdict)

    if problems:
        raise PipelineError(
            f"{stage_id} cannot complete for {episode_id} -- "
            f"deliverable/verdict check failed:\n  - " + "\n  - ".join(problems)
        )


def _verdict_problems(ep: Path, verdict: dict) -> list[str]:
    """Why one declared verdict artifact does not carry a current, passing result."""
    problems: list[str] = []
    vf = ep / verdict["file"]
    text = vf.read_text(encoding="utf-8") if vf.exists() else ""
    if "json_status" in verdict:
        try:
            doc = json.loads(text)
        except Exception as exc:  # noqa: BLE001 - report any parse failure
            return [f"{verdict['file']}: not valid JSON ({exc})"]
        if str(doc.get("status")) != verdict["json_status"]:
            problems.append(
                f"{verdict['file']} status is {doc.get('status')!r}, "
                f"required {verdict['json_status']!r}"
            )
        for key, want in (verdict.get("json_fields") or {}).items():
            if doc.get(key) != want:
                problems.append(
                    f"{verdict['file']} {key!r} is {doc.get(key)!r}, "
                    f"required {want!r}"
                )
        # A machine review records the hash of every file it read; any edit
        # after it ran means its PASS no longer describes what is on disk.
        fresh_field = verdict.get("fresh_inputs_field")
        if fresh_field:
            recorded = doc.get(fresh_field)
            if not isinstance(recorded, dict) or not recorded:
                problems.append(f"{verdict['file']} records no {fresh_field!r} -- "
                                f"re-run the tool that writes it")
            else:
                for rel, digest in recorded.items():
                    p = ep / rel
                    if not p.is_file():
                        problems.append(f"{verdict['file']} reviewed {rel}, which is now missing")
                    elif _sha256(p) != digest:
                        problems.append(f"{rel} changed after {verdict['file']} was written "
                                        f"-- re-run the review")
        return problems

    # A verdict file legitimately accumulates a round-by-round history
    # (REVISE, fix, REVISE, fix, ... PASS) via append, per this repo's own
    # review convention -- only the LAST verdict line in the file is the
    # current one. A blind "does a block pattern appear anywhere" check would
    # permanently fail any episode whose review history contains an earlier,
    # already-superseded REVISE. Compare the position of the last match of
    # each pattern instead.
    pass_pat = verdict.get("pass")
    block_pat = verdict.get("block")
    last_pass_end = None
    last_block_end = None
    if pass_pat:
        for m in re.finditer(pass_pat, text):
            last_pass_end = m.end()
    if block_pat:
        for m in re.finditer(block_pat, text):
            last_block_end = m.end()
    if last_block_end is not None and (
        last_pass_end is None or last_block_end > last_pass_end
    ):
        problems.append(
            f"{verdict['file']} carries a blocking verdict as its most "
            f"recent result (matched /{block_pat}/) -- this stage cannot "
            f"complete; resolve the block or reopen an earlier stage"
        )
    elif pass_pat and last_pass_end is None:
        problems.append(
            f"{verdict['file']} does not carry a passing verdict "
            f"(no line matching /{pass_pat}/)"
        )
    return problems


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def deliverable_digest(slug: str, episode_id: str, stage_id: str) -> dict | None:
    """Snapshot the bytes a stage was completed against: the sorted (path, sha256)
    of every file its stage-gates.json `outputs` resolve to, plus one digest over
    that list. Recorded on the completed_stages entry so a later edit to a
    deliverable is detectable -- an approval covers the bytes it saw, not the path.

    Returns None for a stage with no gate entry or no digestable outputs.

    Outputs that a *later* stage also declares (a shared, append-only deliverable
    like visual/references/manifest.md, written at both 04b and 04c) are excluded:
    a later stage legitimately edits them, so digesting them here guarantees false
    drift. Their integrity is still covered by episode_health's hash check.
    """
    gates = _load_stage_gates()
    try:
        seq = load_state(slug, episode_id).get("stage_sequence", [])
    except PipelineError:
        seq = []
    spec = stage_spec(gates, stage_id, seq)
    if not spec["outputs"]:
        return None

    shared_later: set[str] = set()
    if stage_id in seq:
        for later in seq[seq.index(stage_id) + 1:]:
            for pat in stage_spec(gates, later, seq)["outputs"]:
                if not any(c in pat for c in "*?["):
                    shared_later.add(pat)

    ep = _episode_dir(slug, episode_id)
    files: list[dict] = []
    for pat in spec["outputs"]:
        if pat in shared_later:
            continue
        matches = sorted(ep.glob(pat)) if any(c in pat for c in "*?[") else [ep / pat]
        for p in matches:
            # the state machine's own bookkeeping files are gate outputs of
            # 00-preflight but they are not "deliverables" -- they change on every
            # later operation, so digesting them would guarantee false drift.
            if p.name in _STATE_MACHINE_FILES:
                continue
            if p.is_file():
                files.append({
                    "path": p.relative_to(ep).as_posix(),
                    "sha256": _sha256(p),
                })
    if not files:
        return None
    files.sort(key=lambda f: f["path"])
    payload = "\n".join(f"{f['path']} {f['sha256']}" for f in files)
    return {
        "digest_sha256": hashlib.sha256(payload.encode("utf-8")).hexdigest(),
        "files": files,
    }


def approval_drift(slug: str, episode_id: str) -> list[str]:
    """For each completed stage, report deliverable files that have changed or
    vanished since that stage was last completed. Read-only; advisory.

    Only the *latest* completion entry per stage is checked: a stage that was
    reopened and re-completed keeps its earlier entries as historical evidence,
    and those necessarily predate the current deliverables.

    Report-only by design: a closed episode legitimately gets post-hoc annotations
    (e.g. a superseded-settings note), and this must not turn into a hard failure.
    """
    state = load_state(slug, episode_id)
    ep = _episode_dir(slug, episode_id)
    latest: dict[str, dict] = {}
    for entry in state.get("completed_stages", []):
        latest[entry.get("stage", "?")] = entry  # last wins = most recent completion
    out: list[str] = []
    for stage, entry in latest.items():
        digest = entry.get("deliverable_digest")
        if not digest:
            continue  # newest completion of this stage recorded no digest
        when = entry.get("completed_at", "?")
        for f in digest.get("files", []):
            p = ep / f["path"]
            if not p.is_file():
                out.append(f"{stage} (completed {when}): {f['path']} is GONE since approval")
            elif _sha256(p) != f["sha256"]:
                out.append(f"{stage} (completed {when}): {f['path']} CHANGED since approval")
    return out


def complete_stage(
    slug: str, episode_id: str, stage_id: str, approve: bool = False, note: str = ""
) -> dict:
    with _episode_lock(slug, episode_id):
        state = load_state(slug, episode_id)
        if state["status"] != "open":
            raise PipelineError(f"{episode_id} is {state['status']}, not open")
        if state["next_stage"] != stage_id:
            raise PipelineError(
                f"{episode_id}'s next stage is {state['next_stage']!r}, not {stage_id!r}"
            )
        if stage_owner_gate(slug, stage_id) and not approve:
            raise PipelineError(
                f"{stage_id} is an owner gate for {slug} -- re-run with --approve as the human owner"
            )
        stage_gate_check(slug, episode_id, stage_id)
        seq = state["stage_sequence"]
        idx = seq.index(stage_id)
        digest = deliverable_digest(slug, episode_id, stage_id)
        entry = {
            "stage": stage_id,
            "completed_at": _now(),
            "approved": approve,
            "note": note,
        }
        if digest:
            entry["deliverable_digest"] = digest
        state["completed_stages"].append(entry)
        if idx + 1 < len(seq):
            state["next_stage"] = seq[idx + 1]
        else:
            state["next_stage"] = None
            state["status"] = "closed"
        # log first, then the atomic state write: a crash between them leaves an
        # orphan "completed" log line (harmless, self-explanatory) rather than an
        # advanced state with no record of why.
        _append_log(
            slug,
            episode_id,
            f"completed {stage_id}"
            + (" (owner-approved)" if approve else "")
            + (f" -- {note}" if note else "")
            + (f"; digest {digest['digest_sha256'][:8]}" if digest else "")
            + (f"; next: {state['next_stage']}" if state["next_stage"] else "; episode CLOSED"),
        )
        _save_state(slug, episode_id, state)
        return state


def reopen_stage(
    slug: str, episode_id: str, stage_id: str, *, approve: bool = False, note: str = ""
) -> dict:
    """Return an open episode to an earlier stage after an owner-approved revision.

    Completion entries remain historical evidence.  A later re-completion of a
    rerun stage is intentionally appended as a new entry, while the state log
    records why the pipeline moved backwards.
    """
    if not approve:
        raise PipelineError(
            "reopening an episode requires --approve as the human owner"
        )
    with _episode_lock(slug, episode_id):
        state = load_state(slug, episode_id)
        seq = state.get("stage_sequence", [])
        if stage_id not in seq:
            raise PipelineError(f"{episode_id} has no stage {stage_id!r}")
        target_idx = seq.index(stage_id)
        current = state.get("next_stage")
        current_idx = seq.index(current) if current in seq else len(seq)
        if target_idx >= current_idx:
            raise PipelineError(
                f"{stage_id!r} is not earlier than the current next stage {current!r}"
            )
        previous = current
        state["status"] = "open"
        state["next_stage"] = stage_id
        state.setdefault("revisions", []).append(
            {
                "reopened_at": _now(),
                "from_next_stage": previous,
                "to_stage": stage_id,
                "approved": True,
                "note": note,
            }
        )
        _append_log(
            slug,
            episode_id,
            f"owner-approved revision reopened from {previous} to {stage_id}"
            + (f" -- {note}" if note else ""),
        )
        _save_state(slug, episode_id, state)
        return state
