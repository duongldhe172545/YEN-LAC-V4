import subprocess
import sys
from pathlib import Path


def test_validate_registry_passes():
    repo_root = Path(__file__).resolve().parents[1]
    cmd = [
        sys.executable,
        str(repo_root / "code" / "scripts" / "validate_registry.py"),
        "--repo_root",
        str(repo_root),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    assert res.returncode == 0, f"stdout:\n{res.stdout}\nstderr:\n{res.stderr}"
