from __future__ import annotations

import json
import importlib.util
import os
import shutil
import subprocess
from pathlib import Path

import pytest
import sys

from hyperflow.version import __version__


REPO_ROOT = Path(__file__).resolve().parents[2]
HEAVY_TIMEOUT_SECONDS = 90
LIGHT_TIMEOUT_SECONDS = 30
def _has_setuptools_build_meta() -> bool:
    try:
        return importlib.util.find_spec("setuptools.build_meta") is not None
    except ModuleNotFoundError:
        return False


HAS_SETUPTOOLS_BUILD_META = _has_setuptools_build_meta()


def _venv_console_script(venv_dir: Path) -> Path:
    if sys.platform.startswith("win"):
        return venv_dir / "Scripts" / "hyperflow.exe"
    return venv_dir / "bin" / "hyperflow"


def _smoke_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    env.setdefault("PIP_NO_INPUT", "1")
    return env


def _run_checked(argv: list[str], *, timeout: int, env: dict[str, str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(
            argv,
            cwd=cwd,
            env=env,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=timeout,
        )
    except subprocess.TimeoutExpired as exc:
        output = (exc.stdout or "") if isinstance(exc.stdout, str) else ""
        tail = "\n".join(output.splitlines()[-20:])
        raise AssertionError(f"subprocess timed out after {timeout}s: {' '.join(argv)}\n{tail}") from exc
    except subprocess.CalledProcessError as exc:
        tail = "\n".join((exc.stdout or "").splitlines()[-20:])
        raise AssertionError(f"subprocess failed: {' '.join(argv)}\n{tail}") from exc


def _find_backend_python() -> str:
    candidates = [Path('/opt/pyvenv/bin/python'), Path(sys.executable), Path('/usr/bin/python3')]
    probe = 'import importlib.util; raise SystemExit(0 if importlib.util.find_spec("setuptools.build_meta") else 1)'
    for candidate in candidates:
        if not candidate.exists():
            continue
        completed = subprocess.run(
            [str(candidate), '-c', probe],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=LIGHT_TIMEOUT_SECONDS,
        )
        if completed.returncode == 0:
            return str(candidate)
    return sys.executable


from hyperflow.tests._packaging_smoke import (
    HEAVY_TIMEOUT_SECONDS,
    LIGHT_TIMEOUT_SECONDS,
    REPO_ROOT,
    build_dist_via_backend,
    run_checked,
    smoke_env,
    venv_console_script,
)
from hyperflow.version import __version__


@pytest.mark.skipif(not HAS_SETUPTOOLS_BUILD_META, reason="setuptools.build_meta is required for wheel smoke")
def test_built_wheel_installs_and_runs_outside_repo(tmp_path: Path) -> None:
    dist_dir = tmp_path / "dist"
    venv_dir = tmp_path / "venv"
    env = smoke_env()

    try:
        build_dist_via_backend(dist_dir=dist_dir, env=env, build_fn="build_wheel")

        wheel = next(dist_dir.glob("hyperflow-*.whl"))
        run_checked([sys.executable, "-m", "venv", str(venv_dir)], env=env, timeout=HEAVY_TIMEOUT_SECONDS)

        py = venv_dir / "bin" / "python"
        cli = venv_console_script(venv_dir)
        run_checked([str(py), "-m", "pip", "install", str(wheel)], env=env, timeout=HEAVY_TIMEOUT_SECONDS)

        outside_dir = tmp_path / "outside_repo"
        outside_dir.mkdir()

        version = run_checked([str(py), "-m", "hyperflow.interface.cli", "--version"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        assert version.stdout.strip() == f"Hyperflow {__version__}"

        package_version = run_checked([str(py), "-m", "hyperflow", "--version"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        assert package_version.stdout.strip() == f"Hyperflow {__version__}"

        console_version = run_checked([str(cli), "--version"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        assert console_version.stdout.strip() == f"Hyperflow {__version__}"

        run = run_checked([str(py), "-m", "hyperflow.interface.cli", "🌈💎🔥🧠🔀⚡ wheel smoke"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        payload = json.loads(run.stdout)
        assert payload["run_id"]
        assert payload["contract"]["schema"] == "hyperflow/edde-contract/v1"

        package_run = run_checked([str(py), "-m", "hyperflow", "🌈💎🔥🧠🔀⚡ wheel smoke"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        package_payload = json.loads(package_run.stdout)
        assert package_payload["run_id"]
        assert package_payload["contract"]["schema"] == "hyperflow/edde-contract/v1"

        console_run = run_checked([str(cli), "🌈💎🔥🧠🔀⚡ wheel smoke"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        console_payload = json.loads(console_run.stdout)
        assert console_payload["run_id"]
        assert console_payload["contract"]["schema"] == "hyperflow/edde-contract/v1"

        config = run_checked(
            [
                str(py),
                "-c",
                "from hyperflow.config import get_canonical_emoji_library_config; print(get_canonical_emoji_library_config()['canonical_signature']['emoji'])",
            ],
            cwd=outside_dir,
            env=env,
            timeout=LIGHT_TIMEOUT_SECONDS,
        )
        assert config.stdout.strip() == "🌈💎🔥🧠🔀⚡"
    finally:
        shutil.rmtree(venv_dir, ignore_errors=True)
        shutil.rmtree(REPO_ROOT / "build", ignore_errors=True)
        shutil.rmtree(REPO_ROOT / "dist", ignore_errors=True)
        shutil.rmtree(REPO_ROOT / "hyperflow.egg-info", ignore_errors=True)
