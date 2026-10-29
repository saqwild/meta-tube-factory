"""Self-locating path constants. No git dependency."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANNEL_PROFILES_DIR = ROOT / "channel_profiles"
STAGES_DIR = ROOT / "pipeline" / "stages"
EPISODES_DIR = ROOT / "episodes"
SCHEMAS_DIR = ROOT / "pipeline" / "schemas"
