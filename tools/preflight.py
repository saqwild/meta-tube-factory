#!/usr/bin/env python3
"""preflight -> pick channel -> load channel profile -> walk stages to completion.

Usage:
    python tools/preflight.py                          interactive: pick channel, resume or start
    python tools/preflight.py list                      list every channel + its episodes
    python tools/preflight.py new <channel_slug>         start a new episode
    python tools/preflight.py resume <channel_slug> <episode_id>
    python tools/preflight.py complete <channel_slug> <episode_id> <stage_id> [--approve] [--note "..."]
    python tools/preflight.py reopen <channel_slug> <episode_id> <stage_id> --approve [--note "..."]
    python tools/preflight.py health <channel_slug> <episode_id>    read-only end-to-end consistency check
"""
import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import episode_state as es
from project_paths import ROOT, STAGES_DIR


def _print_next(slug: str, state: dict) -> None:
    channel = es.load_channel(slug)
    print(f"\nChannel: {channel['channel']['name']}  ({slug})")
    print(f"Episode: {state['episode_id']}  status={state['status']}")
    if state["status"] == "closed":
        print("This episode is CLOSED. Nothing further to do.")
        return
    stage = state["next_stage"]
    gate = es.stage_owner_gate(slug, stage)
    contract = STAGES_DIR / f"{stage}.md"
    print(f"Next stage: {stage}" + ("  [OWNER GATE]" if gate else ""))
    print(f"Contract:   {contract.relative_to(ROOT)}")
    print(f"Channel profile: channel_profiles/{slug}/channel.json")
    print(
        f"\nWhen done, run:\n"
        f'  python tools/preflight.py complete {slug} {state["episode_id"]} {stage}'
        + (" --approve" if gate else "")
    )


def cmd_list(_args) -> None:
    slugs = es.preflight_check()
    for slug in slugs:
        channel = es.load_channel(slug)
        eps = es.list_episodes(slug)
        print(f"\n{channel['channel']['name']}  ({slug})  models={channel['models']['image']}/{channel['models']['video']}")
        if not eps:
            print("  (no episodes yet)")
        for ep in eps:
            print(f"  {ep['episode_id']}: status={ep['status']} next={ep['next_stage']}")


def cmd_new(args) -> None:
    es.preflight_check()
    state = es.create_episode(args.channel_slug)
    _print_next(args.channel_slug, state)


def cmd_resume(args) -> None:
    es.preflight_check()
    state = es.load_state(args.channel_slug, args.episode_id)
    _print_next(args.channel_slug, state)


def cmd_complete(args) -> None:
    es.preflight_check()
    state = es.complete_stage(
        args.channel_slug,
        args.episode_id,
        args.stage_id,
        approve=args.approve,
        note=args.note or "",
    )
    _print_next(args.channel_slug, state)


def cmd_reopen(args) -> None:
    es.preflight_check()
    drift = es.approval_drift(args.channel_slug, args.episode_id)
    if drift:
        print("Note -- deliverables changed since an approval:")
        for line in drift:
            print(f"  {line}")
        print()
    state = es.reopen_stage(
        args.channel_slug,
        args.episode_id,
        args.stage_id,
        approve=args.approve,
        note=args.note or "",
    )
    _print_next(args.channel_slug, state)


def cmd_health(args) -> None:
    es.preflight_check()
    import episode_health
    raise SystemExit(episode_health.main(
        ["--channel", args.channel_slug, "--episode", args.episode_id]))


def _prompt(question: str) -> str:
    try:
        return input(question).strip()
    except EOFError:
        print(
            "\nNo input available (stdin is not a terminal). Use the subcommands "
            "instead:\n  python tools/preflight.py list\n"
            "  python tools/preflight.py new <channel_slug>\n"
            "  python tools/preflight.py resume <channel_slug> <episode_id>",
            file=sys.stderr,
        )
        raise SystemExit(2)


def _interactive() -> None:
    slugs = es.preflight_check()
    print("Preflight OK. Channels:")
    for i, slug in enumerate(slugs, 1):
        name = es.load_channel(slug)["channel"]["name"]
        print(f"  [{i}] {name}  ({slug})")
    choice = _prompt("Select channel: ")
    try:
        slug = slugs[int(choice) - 1]
    except (ValueError, IndexError):
        print("Not a valid choice.")
        return

    open_eps = [e for e in es.list_episodes(slug) if e["status"] == "open"]
    if open_eps:
        most_recent = max(open_eps, key=lambda e: e["updated_at"])
        print(f"\nMost recent open episode: {most_recent['episode_id']} (next: {most_recent['next_stage']})")
        ans = _prompt("Resume it? [Y/n] or type 'new': ").lower()
        if ans == "new":
            state = es.create_episode(slug)
        else:
            state = most_recent
    else:
        print("No open episodes for this channel -- starting a new one.")
        state = es.create_episode(slug)

    _print_next(slug, state)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list").set_defaults(func=cmd_list)

    p_new = sub.add_parser("new")
    p_new.add_argument("channel_slug")
    p_new.set_defaults(func=cmd_new)

    p_resume = sub.add_parser("resume")
    p_resume.add_argument("channel_slug")
    p_resume.add_argument("episode_id")
    p_resume.set_defaults(func=cmd_resume)

    p_complete = sub.add_parser("complete")
    p_complete.add_argument("channel_slug")
    p_complete.add_argument("episode_id")
    p_complete.add_argument("stage_id")
    p_complete.add_argument("--approve", action="store_true")
    p_complete.add_argument("--note", default="")
    p_complete.set_defaults(func=cmd_complete)

    p_reopen = sub.add_parser("reopen")
    p_reopen.add_argument("channel_slug")
    p_reopen.add_argument("episode_id")
    p_reopen.add_argument("stage_id")
    p_reopen.add_argument("--approve", action="store_true")
    p_reopen.add_argument("--note", default="")
    p_reopen.set_defaults(func=cmd_reopen)

    p_health = sub.add_parser("health")
    p_health.add_argument("channel_slug")
    p_health.add_argument("episode_id")
    p_health.set_defaults(func=cmd_health)

    args = parser.parse_args()
    try:
        if args.command is None:
            _interactive()
        else:
            args.func(args)
    except es.PipelineError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
