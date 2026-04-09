from __future__ import annotations

import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
HEAVY_TIMEOUT_SECONDS = 90
LIGHT_TIMEOUT_SECONDS = 30


def venv_console_script(venv_dir: Path) -> Path:
    if sys.platform.startswith("win"):
        return venv_dir / "Scripts" / "hyperflow.exe"
    return venv_dir / "bin" / "hyperflow"


def smoke_env() -> dict[str, str]:
    env = os.environ.copy()
    env.pop("PYTHONPATH", None)
    env.setdefault("PIP_DISABLE_PIP_VERSION_CHECK", "1")
    env.setdefault("PIP_NO_INPUT", "1")
    return env


def run_checked(
    argv: list[str],
    *,
    timeout: int,
    env: dict[str, str],
    cwd: Path | None = None,
) -> subprocess.CompletedProcess[str]:
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


def _find_backend_python() -> tuple[str | None, str]:
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
            return str(candidate), ""
    return _bootstrap_backend_python()


def _bootstrap_backend_python() -> tuple[str | None, str]:
    venv_dir = Path(tempfile.gettempdir()) / "hyperflow-packaging-backend"
    if sys.platform.startswith("win"):
        venv_python = venv_dir / "Scripts" / "python.exe"
    else:
        venv_python = venv_dir / "bin" / "python"

    env = smoke_env()
    try:
        run_checked([sys.executable, "-m", "venv", str(venv_dir)], timeout=HEAVY_TIMEOUT_SECONDS, env=env)
        run_checked([str(venv_python), "-m", "pip", "install", "--upgrade", "pip"], timeout=HEAVY_TIMEOUT_SECONDS, env=env)
        run_checked(
            [str(venv_python), "-m", "pip", "install", "setuptools>=68", "wheel"],
            timeout=HEAVY_TIMEOUT_SECONDS,
            env=env,
        )
    except AssertionError as exc:
        return None, str(exc)

    probe = 'import importlib.util; raise SystemExit(0 if importlib.util.find_spec("setuptools.build_meta") else 1)'
    completed = subprocess.run(
        [str(venv_python), '-c', probe],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        timeout=LIGHT_TIMEOUT_SECONDS,
    )
    if completed.returncode == 0:
        return str(venv_python), ""
    return None, "bootstrap venv does not expose setuptools.build_meta after setup"


def build_dist_via_backend(
    *,
    dist_dir: Path,
    env: dict[str, str],
    build_fn: str,
) -> None:
    dist_dir.mkdir(parents=True, exist_ok=True)
    build_python, reason = _find_backend_python()
    if build_python is None:
        suffix = f" ({reason})" if reason else ""
        pytest.skip(f"setuptools.build_meta is not available in this environment{suffix}")

    call_args = 'r"' + str(dist_dir) + '", None'
    if build_fn == "build_wheel":
        call_args += ", None"

    backend_code = (
        f'from setuptools.build_meta import {build_fn}; '
        f'name = {build_fn}({call_args}); '
        'print(name)'
    )
    run_checked([build_python, '-c', backend_code], cwd=REPO_ROOT, env=env, timeout=HEAVY_TIMEOUT_SECONDS)
