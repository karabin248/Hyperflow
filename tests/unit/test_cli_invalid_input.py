from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from hyperflow.interface.cli import main
from hyperflow.language.command_builder import build_command


def test_build_command_rejects_empty_input() -> None:
    with pytest.raises(ValueError, match="Input is required"):
        build_command("   ")


def test_cli_rejects_empty_input(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "argv", ["hyperflow"])
    with pytest.raises(SystemExit, match="Input is required"):
        main()


def test_cli_save_failure_is_user_facing(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    bad_target = tmp_path / "output-dir"
    bad_target.mkdir()
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "hyperflow",
            "🌈💎🔥🧠🔀⚡ Task: prepare an MVP plan",
            "--save",
            str(bad_target),
        ],
    )

    with pytest.raises(SystemExit, match="Unable to save output payload"):
        main()


def test_cli_rejects_conflicting_output_modes() -> None:
    completed = subprocess.run(
        [
            sys.executable,
            "-m",
            "hyperflow.interface.cli",
            "🌈💎🔥🧠🔀⚡ Task: prepare an MVP plan",
            "--json",
            "--pretty",
        ],
        capture_output=True,
        text=True,
    )

    assert completed.returncode == 2
    assert "not allowed with argument" in completed.stderr
