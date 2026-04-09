import json
import subprocess
import sys
from pathlib import Path


def test_save_payload_shape(tmp_path: Path):
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    file_path = tmp_path / "output.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hyperflow.interface.cli",
            raw,
            "--save",
            str(file_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    loaded = json.loads(file_path.read_text(encoding="utf-8"))
    assert loaded["command"]["intent"] == "planning"
    assert loaded["result"]["mode"] == "fusion"
    assert loaded["run_id"]
    assert loaded["contract"]["schema"] == "hyperflow/edde-contract/v1"
    assert loaded["contract"] == loaded["result"]["edde_contract"]


def test_save_creates_parent_directories(tmp_path: Path):
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: save the result to a nested directory "
        "Goal: confirm parent auto-create behavior"
    )

    file_path = tmp_path / "nested" / "deep" / "output.json"
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hyperflow.interface.cli",
            raw,
            "--save",
            str(file_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 0
    assert file_path.exists()
    loaded = json.loads(file_path.read_text(encoding="utf-8"))
    assert loaded["run_id"]
    assert loaded["contract"]["schema"] == "hyperflow/edde-contract/v1"


def test_json_flag_matches_default_json_output() -> None:
    raw = "🌈💎🔥🧠🔀⚡ Task: return the result in JSON"

    default_run = subprocess.run(
        [sys.executable, "-m", "hyperflow.interface.cli", raw],
        check=True,
        capture_output=True,
        text=True,
    )
    json_run = subprocess.run(
        [sys.executable, "-m", "hyperflow.interface.cli", raw, "--json"],
        check=True,
        capture_output=True,
        text=True,
    )

    default_payload = json.loads(default_run.stdout)
    json_payload = json.loads(json_run.stdout)

    assert default_payload["intent"] == json_payload["intent"]
    assert default_payload["mode"] == json_payload["mode"]
    assert default_payload["output_type"] == json_payload["output_type"]
    assert default_payload["command"] == json_payload["command"]
    assert default_payload["contract"]["schema"] == json_payload["contract"]["schema"]
