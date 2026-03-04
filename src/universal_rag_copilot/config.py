"""Small config helpers for local fixture paths."""

from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIXTURES_DIR = REPO_ROOT / "fixtures"
OUTPUTS_DIR = REPO_ROOT / "outputs"
