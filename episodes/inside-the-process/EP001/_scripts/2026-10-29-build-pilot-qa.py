"""Build qa/ltx-pilot-qa.json from owner-watched pilot verdicts.

Verdicts are the owner's (recorded in qa/pilot-qa.md after each watched
clip); this script only structures them against the 04h check list.
Run from repo root.
"""
import datetime
import hashlib
import json
import pathlib

EP = pathlib.Path(__file__).resolve().parents[1]
PKG = EP / "exports" / "ltx-render-package" / "render-manifest.json"
OUT = EP / "qa" / "ltx-pilot-qa.json"

manifest = json.loads(PKG.read_text(encoding="utf-8"))
settings = manifest["settings"]
pkg_sha = hashlib.sha256(PKG.read_bytes()).hexdigest()


def chk(note):
    return {"result": "PASS", "note": note}


CLIPS = [
    {
        "clip": "SC01",
        "render_path": "renders/ltx-inbox/s01_20261101010657.mp4",
        "coverage": ["opening", "prop_interaction"],
        "checks": {
            "beat_adherence": chk("The one linen cloth settles in one hand at the adult's side and the risen dough stays fully uncovered, as beaten."),
            "frame0_fidelity": chk("Clip starts from the approved CAST-002 still; identity, kitchen and capsule match frame 0."),
            "dialogue": chk("Control narration only, the authorised SC01 lines, audible and unhurried."),
            "speaker_binding": chk("The adult's mouth stays closed while Control narrates off-screen."),
            "identity_and_cast_count": chk("Exactly one adult, matching the CAST-002 sheet (short tight curly hair, navy hoodie)."),
            "prop_interaction": chk("One cloth, one bowl; the cloth never covers the dough and no prop duplicates."),
            "environment_and_camera": chk("Kitchen stays stable; the push-in ends on the risen dough and the descending capsule."),
            "audio": chk("Quiet kitchen room tone with cloth rustle; trailing silence is logged for the 06a trim, not a render fault."),
            "artifacts": chk("No burned-in text, no anatomy failures; hands are clean with short nails."),
        },
        "verdict": "PASS",
    },
    {
        "clip": "SC02",
        "render_path": "renders/ltx-inbox/s02_20261031222309.mp4",
        "coverage": ["multi_character"],
        "checks": {
            "beat_adherence": chk("The Explorer turns to camera and asks his question inside the wet mixed mass, as beaten."),
            "frame0_fidelity": chk("Clip starts from the approved still; capsule rests behind him in the dough."),
            "dialogue": chk("Explorer question and Control answer are the authorised lines, intelligible over helmet radio."),
            "speaker_binding": chk("Only the Explorer's line is delivered on-screen; Control answers off-screen with the visor closed."),
            "identity_and_cast_count": chk("One Explorer, opaque black full-face visor, no face visible, no extra figure."),
            "prop_interaction": chk("No props touched; hands stay empty as blocked."),
            "environment_and_camera": chk("Wet mass and flour pockets stay stable; only the named ambient drift moves."),
            "audio": chk("Clean dialogue over dough ambience; any tail silence is a 06a trim item."),
            "artifacts": chk("No burned-in text; suit and helmet render clean."),
        },
        "verdict": "PASS",
    },
    {
        "clip": "SC05",
        "render_path": "renders/ltx-inbox/s05_20261101011309.mp4",
        "coverage": ["dense_dialogue"],
        "checks": {
            "beat_adherence": chk("Bubbles inflate and the net stretches in a slow swell while the Explorer stays settled on the mass."),
            "frame0_fidelity": chk("Starts from the approved stretched-net still; the Explorer holds his frame-0 spot at the edge."),
            "dialogue": chk("Explorer line and Control's long answer are the authorised words at a natural pace."),
            "speaker_binding": chk("The Explorer speaks his line only; Control's answer is off-screen and his mouth stays closed behind the visor."),
            "identity_and_cast_count": chk("Exactly one Explorer for the whole clip; no second figure appears on the fixed re-render."),
            "prop_interaction": chk("Hands stay empty; the net is never gripped."),
            "environment_and_camera": chk("The tilt-up ends on the stretched gluten net and inflated bubbles, not on the Explorer."),
            "audio": chk("Stretching creaks under clear dialogue; visor stays opaque so no lip-sync artifact is visible."),
            "artifacts": chk("No face appears through the visor on the re-render; no burned-in text."),
        },
        "verdict": "PASS",
    },
    {
        "clip": "SC08",
        "render_path": "renders/ltx-inbox/s08_20261031234801.mp4",
        "coverage": ["continuity"],
        "checks": {
            "beat_adherence": chk("Oven spring: bubbles expand fast and the dome rises while the Explorer braces, as beaten."),
            "frame0_fidelity": chk("Starts from the approved oven-heat still with the Explorer braced at the edge."),
            "dialogue": chk("Explorer line and Control's oven-spring answer are the authorised words."),
            "speaker_binding": chk("Explorer delivers his line; Control answers off-screen, Explorer mouth closed behind the visor."),
            "identity_and_cast_count": chk("One Explorer, visor opaque throughout the heat sequence."),
            "prop_interaction": chk("No prop contact; bracing reads against the foam only."),
            "environment_and_camera": chk("Heat glow and steam stay stable; the dolly ends on the expanding bubbles and rising dome."),
            "audio": chk("Low oven roar under clear dialogue, clean tail."),
            "artifacts": chk("No burned-in text, no anatomy or suit artifacts."),
        },
        "verdict": "PASS",
    },
    {
        "clip": "SC12",
        "render_path": "renders/ltx-inbox/s12_20261031235636.mp4",
        "coverage": ["warm_close"],
        "checks": {
            "beat_adherence": chk("The cooled loaf is held steady and the cut slice reveals the finished crumb, as beaten."),
            "frame0_fidelity": chk("Starts from the approved close-up still: loaf on the wooden board, one slice cut."),
            "dialogue": chk("Closing lines are the authorised words, delivered inside the clip."),
            "speaker_binding": chk("Speech binds to the adult at the board; no other mouth moves."),
            "identity_and_cast_count": chk("Only the adult's hands and the loaf are in frame; exactly the blocked cast."),
            "prop_interaction": chk("One hand holds the loaf steady with short clean nails and minimal arm hair; no duplicate hands."),
            "environment_and_camera": chk("Camera stays on the bread zoom the owner asked for; kitchen background stable."),
            "audio": chk("Quiet kitchen tone, clean start and tail."),
            "artifacts": chk("No burned-in text; crumb and crust render clean."),
        },
        "verdict": "PASS",
    },
]

doc = {
    "schema_version": 1,
    "episode_id": "EP001",
    "watched_by": "owner (saqwild)",
    "watched_at_utc": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "package_manifest_sha256": pkg_sha,
    "settings_profile": {
        "workflow": settings["workflow"],
        "megapixels": settings["megapixels"],
        "duration_seconds": settings["duration_seconds"],
        "cfg": settings["cfg"],
        "cfg_refine": settings["cfg_refine"],
        "cfg_audio": settings["cfg_audio"],
        "img_compression": settings["img_compression"],
    },
    "status": "PASS",
    "clips": CLIPS,
    "open_question_findings": [
        {
            "question": "frame0_adherence_strictness",
            "observation": "On the fixed re-renders (SC01, SC05, SC06, SC07, SC10, SC11) the clips hold their approved frame 0 when the prompt states a positive stay-delta; the earlier drift cases all traced to prompt wording that contradicted or under-specified the still.",
            "verdict": "confirmed_still_true",
            "evidence_clips": ["SC01", "SC05", "SC06", "SC07", "SC10", "SC11"],
        },
        {
            "question": "dialogue_occupancy_at_20s",
            "observation": "Owner viewing found short dialogue with dead-silence tails on several 20 s clips (SC02-SC06 batch); the fix is a 06a assembly trim, so occupancy is not yet measured from transcripts.",
            "verdict": "inconclusive",
            "evidence_clips": ["SC02", "SC03", "SC04", "SC05", "SC06"],
        },
    ],
}

OUT.write_text(json.dumps(doc, indent=2) + "\n", encoding="utf-8")
print({"wrote": str(OUT), "clips": len(CLIPS), "status": doc["status"]})
