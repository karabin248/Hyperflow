from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from hyperflow.version import get_version


def _resolve_console_script() -> str | None:
    direct = Path(sys.executable).with_name("hyperflow")
    if direct.exists():
        return str(direct)
    scripts_dir = Path(__import__("sysconfig").get_path("scripts")) / "hyperflow"
    if scripts_dir.exists():
        return str(scripts_dir)
    return shutil.which("hyperflow")


def test_module_entrypoint_version_matches_console_script() -> None:
    expected = f"Hyperflow {get_version()}"

    package_module = subprocess.run(
        [sys.executable, "-m", "hyperflow", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    cli_module = subprocess.run(
        [sys.executable, "-m", "hyperflow.interface.cli", "--version"],
        check=True,
        capture_output=True,
        text=True,
    )
    console_script = _resolve_console_script()
    if console_script is None:
        pytest.skip("hyperflow console script is not installed in the active environment")

    console = subprocess.run(
        [console_script, "--version"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert package_module.stdout.strip() == expected
    assert cli_module.stdout.strip() == expected
    assert console.stdout.strip() == expected
    assert package_module.stdout == cli_module.stdout == console.stdout



def test_module_help_uses_canonical_prog_name() -> None:
    package_help = subprocess.run(
        [sys.executable, "-m", "hyperflow", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )
    cli_help = subprocess.run(
        [sys.executable, "-m", "hyperflow.interface.cli", "--help"],
        check=True,
        capture_output=True,
        text=True,
    )

    assert package_help.stdout.startswith("usage: hyperflow ")
    assert cli_help.stdout.startswith("usage: hyperflow ")
    assert "__main__.py" not in package_help.stdout
    assert "cli.py" not in cli_help.stdout
