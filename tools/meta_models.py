"""Meta Model API execution layer (standard library only).

Centralizes the real Meta model names and roles for hackathon work so every
tool builds requests from one place. Reads the API key from the environment
only -- never commit a key, never log one.

Official behavior this relies on (dev.meta.ai/docs/quickstart):
  * base URL: https://api.meta.ai/v1
  * key env var: MODEL_API_KEY (META_API_KEY accepted as a fallback alias)
  * auth: Authorization: Bearer <key>
  * text/reasoning calls: POST {base}/responses (Responses API)

Endpoint shapes verified against dev.meta.ai/docs on 2026-10-29:
  * image: POST {base}/images/generations (model muse-image-1.0)
  * segment: POST {base}/responses (model sam-3.1, message input)
  * transcribe: POST {base}/asr/transcribe?sessionId=... (multipart,
    model muse-voice-transcribe-1.0, WAV only)
Muse Glimmer and Muse Spark Open are open-weight, self-hosted only --
they have no Model API model ID and are not callable from here.
"""

import json
import os
import urllib.error
import urllib.request

BASE_URL = os.environ.get("META_MODEL_API_BASE_URL", "https://api.meta.ai/v1")

MODEL_IDS = {
    "muse_spark": "muse-spark-1.3",
    "muse_wonder": "muse-wonder-1.0",
    "muse_image": "muse-image-1.0",
    "muse_voice_transcribe": "muse-voice-transcribe-1.0",
    "sam": "sam-3.1",
    # Open-weight only (dev.meta.ai/docs/models): no Model API ID.
    "muse_glimmer": None,
    "muse_spark_open": None,
}

ROLES = {
    "reasoning": "muse_spark",
    "creative": "muse_wonder",
    "image": "muse_image",
    "transcribe": "muse_voice_transcribe",
    "segment": "sam",
    "local_fast": "muse_glimmer",
    "local_open": "muse_spark_open",
}

DOC_PATHS = {
    "quickstart": "dev.meta.ai/docs/quickstart",
    "image": "dev.meta.ai/docs/image-generation",
    "speech": "dev.meta.ai/docs/speech-to-text",
    "segmentation": "dev.meta.ai/docs/media-segmentation",
    "open_weights": "dev.meta.ai/docs/open-weight-models",
}

# Per-step allocation for hackathon work. Keys are pipeline stage ids;
# values are ROLES keys. The user's short names map as: reasoning ->
# muse-spark-1.3 (the bare string "muse-spark" is not a model ID),
# creative -> muse-wonder, image -> muse-image, segment -> sam-3.1,
# transcribe -> muse-voice-transcribe.
STAGE_ALLOCATION = {
    "01-ideation": "reasoning",
    "01b-coverage-scan": "reasoning",
    "02-research": "reasoning",
    "02a-sourcing": "reasoning",
    "02b-compliance": "reasoning",
    "03a-writer": "creative",
    "03b-script-review": "reasoning",
    "04a-visual-brief": "creative",
    "04b-character-refs": "image",
    "04c-scene-refs": "image",
    "04d-shot-plan": "reasoning",
    "04e-storyboard": "image",
    "04f-ltx-prompt-draft": "reasoning",
    "04f2-frame0-stills": "image",
    "04f3-ltx-prompt-final": "reasoning",
    "04h-ltx-pilot-qa": "segment",
    "05a-render-qa": "transcribe",
    "06-distribution-metadata": "reasoning",
}

# Roles callable over Meta Model API from this module.
WIRED_ROLES = {"reasoning", "creative", "image", "segment", "transcribe"}
# Open-weight roles: self-hosted only, no Model API endpoint.
UNWIRED_ROLES = {"local_fast", "local_open"}


def resolve_role(role: str) -> str:
    """Return the concrete Model API model ID for a role name."""
    key = ROLES.get(role)
    if key is None:
        raise ValueError(f"Unknown role {role!r}; known: {sorted(ROLES)}")
    model_id = MODEL_IDS[key]
    if model_id is None:
        raise ValueError(f"Role {role!r} is open-weight/self-hosted; no Model API model ID")
    return model_id


def model_for_stage(stage_id: str) -> str:
    """Return the concrete model ID allocated to a pipeline stage."""
    role = STAGE_ALLOCATION.get(stage_id)
    if role is None:
        raise ValueError(f"No Meta allocation for stage {stage_id!r}")
    return resolve_role(role)


def _load_dotenv() -> None:
    """Load MODEL_API_KEY from a local .env if not already in the env."""
    if os.environ.get("MODEL_API_KEY") or os.environ.get("META_API_KEY"):
        return
    for candidate in (os.path.join(os.getcwd(), ".env"),
                      os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")):
        try:
            with open(candidate, encoding="utf-8") as fh:
                for line in fh:
                    if "=" in line and not line.lstrip().startswith("#"):
                        k, v = line.strip().split("=", 1)
                        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
            return
        except OSError:
            continue


def api_key() -> str:
    """Return the Model API key from the environment. Never logs it."""
    _load_dotenv()
    key = os.environ.get("MODEL_API_KEY") or os.environ.get("META_API_KEY")
    if not key:
        raise RuntimeError(
            "No Model API key found. Export MODEL_API_KEY "
            "(see dev.meta.ai/docs/quickstart)."
        )
    return key


def config_summary() -> dict:
    """Safe-to-print config: base URL, model IDs, and key presence only."""
    _load_dotenv()
    present = bool(os.environ.get("MODEL_API_KEY") or os.environ.get("META_API_KEY"))
    return {"base_url": BASE_URL, "models": dict(MODEL_IDS), "key_present": present}


def _post_json(path: str, payload: dict, timeout_s: int = 120) -> dict:
    body = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{BASE_URL}{path}",
        data=body,
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"Model API HTTP {exc.code}: {detail}") from exc


def responses_create(model_id: str, input_text, timeout_s: int = 120) -> dict:
    """POST one Responses API call and return the decoded JSON body."""
    return _post_json("/responses", {"model": model_id, "input": input_text}, timeout_s)


def image_generate(prompt: str, size: str | None = None, n: int = 1, timeout_s: int = 300) -> dict:
    """POST /images/generations with muse-image-1.0 (docs: image-generation)."""
    payload: dict = {"model": resolve_role("image"), "prompt": prompt, "n": n}
    if size:
        payload["size"] = size
    return _post_json("/images/generations", payload, timeout_s)


def segment(image_url: str, prompt: str, timeout_s: int = 300) -> dict:
    """POST /responses with sam-3.1 (docs: media-segmentation)."""
    message = {
        "type": "message",
        "role": "user",
        "content": [
            {"type": "input_text", "text": prompt},
            {"type": "input_image", "image_url": image_url},
        ],
    }
    return _post_json("/responses", {"model": resolve_role("segment"), "input": [message]}, timeout_s)


def transcribe(wav_path: str, session_id: str = "vidgen-meta", mode: str = "DIARIZATION",
               timeout_s: int = 600) -> dict:
    """POST /asr/transcribe multipart (docs: speech-to-text). WAV only."""
    import uuid

    with open(wav_path, "rb") as fh:
        audio = fh.read()
    boundary = f"----vidgen{uuid.uuid4().hex}"
    settings = json.dumps({"mode": mode, "model": resolve_role("transcribe"), "audioEncoding": "WAV"})
    parts = [
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"request\"\r\n"
        f"Content-Type: application/json\r\n\r\n{settings}\r\n".encode(),
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"audio\"; "
        f"filename=\"audio.wav\"\r\nContent-Type: audio/wav\r\n\r\n".encode() + audio + b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    req = urllib.request.Request(
        f"{BASE_URL}/asr/transcribe?sessionId={session_id}",
        data=b"".join(parts),
        headers={
            "Authorization": f"Bearer {api_key()}",
            "Content-Type": f"multipart/form-data; boundary={boundary}",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout_s) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        raise RuntimeError(f"Model API HTTP {exc.code}: {detail}") from exc


def main(argv=None) -> int:
    """CLI: config | allocation | smoke | call | image | segment | transcribe."""
    import argparse

    parser = argparse.ArgumentParser(description="Meta Model API client")
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("config", help="print safe config (no key value)")
    sub.add_parser("allocation", help="print stage -> model allocation")
    sub.add_parser("smoke", help="one cheap reasoning call to validate key/model")
    call = sub.add_parser("call", help="one Responses API call (reasoning/creative)")
    call.add_argument("--role", default="reasoning", choices=["reasoning", "creative"])
    call.add_argument("--input", required=True)
    img = sub.add_parser("image", help="one muse-image-1.0 generation")
    img.add_argument("--prompt", required=True)
    img.add_argument("--size", default=None)
    img.add_argument("--n", type=int, default=1)
    img.add_argument("--out", default=None)
    seg = sub.add_parser("segment", help="one sam-3.1 segmentation")
    seg.add_argument("--prompt", required=True)
    seg.add_argument("--image-url", required=True)
    trn = sub.add_parser("transcribe", help="one muse-voice-transcribe-1.0 file transcription")
    trn.add_argument("--file", required=True)
    trn.add_argument("--session-id", default="vidgen-meta")
    args = parser.parse_args(argv)

    try:
        if args.cmd == "config":
            print(json.dumps(config_summary(), indent=2))
            return 0
        if args.cmd == "allocation":
            table = {s: model_for_stage(s) for s in sorted(STAGE_ALLOCATION)}
            print(json.dumps(table, indent=2))
            return 0
        if args.cmd == "smoke":
            result = responses_create(resolve_role("reasoning"), "Reply with: ok")
            print(json.dumps({"model": resolve_role("reasoning"), "response": result}, indent=2)[:2000])
            return 0
        if args.cmd == "call":
            result = responses_create(resolve_role(args.role), args.input)
            print(json.dumps({"model": resolve_role(args.role), "response": result}, indent=2)[:4000])
            return 0
        if args.cmd == "image":
            result = image_generate(args.prompt, size=args.size, n=args.n)
            if args.out:
                import base64 as _b64
                import pathlib

                data = (result.get("data") or [{}])[0]
                raw = _b64.b64decode(data["b64_json"]) if data.get("b64_json") else b""
                pathlib.Path(args.out).parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(args.out).write_bytes(raw)
                print(json.dumps({"model": resolve_role("image"), "saved": args.out, "bytes": len(raw)}))
            else:
                print(json.dumps({"model": resolve_role("image"), "response": result}, indent=2)[:4000])
            return 0
        if args.cmd == "segment":
            result = segment(args.image_url, args.prompt)
            print(json.dumps({"model": resolve_role("segment"), "response": result}, indent=2)[:4000])
            return 0
        if args.cmd == "transcribe":
            result = transcribe(args.file, session_id=args.session_id)
            print(json.dumps({"model": resolve_role("transcribe"), "response": result}, indent=2)[:4000])
            return 0
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"error: {exc}")
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
