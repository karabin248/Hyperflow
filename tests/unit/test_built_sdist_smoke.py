from __future__ import annotations

import json
import importlib.util
import os
import shutil
from pathlib import Path

import pytest
import sys

from hyperflow.tests._packaging_smoke import (
    HEAVY_TIMEOUT_SECONDS,
    LIGHT_TIMEOUT_SECONDS,
    REPO_ROOT,
    build_dist_via_backend,
    smoke_env,
    run_checked,
    venv_console_script,
)
from hyperflow.version import __version__


def _has_setuptools_build_meta() -> bool:
    try:
        return importlib.util.find_spec("setuptools.build_meta") is not None
    except ModuleNotFoundError:
        return False


HAS_SETUPTOOLS_BUILD_META = _has_setuptools_build_meta()


@pytest.mark.skipif(not HAS_SETUPTOOLS_BUILD_META, reason="setuptools.build_meta is required for sdist smoke")
def test_built_sdist_installs_and_runs_outside_repo(tmp_path: Path) -> None:
    dist_dir = tmp_path / "sdist"
    venv_dir = tmp_path / "venv"
    env = smoke_env()

    try:
        build_dist_via_backend(dist_dir=dist_dir, env=env, build_fn="build_sdist")

        sdist = next(dist_dir.glob("hyperflow-*.tar.gz"))
        run_checked([sys.executable, "-m", "venv", str(venv_dir)], env=env, timeout=HEAVY_TIMEOUT_SECONDS)

        py = venv_dir / "bin" / "python"
        cli = venv_console_script(venv_dir)
        run_checked([str(py), "-m", "pip", "install", str(sdist)], env=env, timeout=HEAVY_TIMEOUT_SECONDS)

        outside_dir = tmp_path / "outside_repo"
        outside_dir.mkdir()

        version = run_checked([str(py), "-m", "hyperflow.interface.cli", "--version"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        assert version.stdout.strip() == f"Hyperflow {__version__}"

        package_version = run_checked([str(py), "-m", "hyperflow", "--version"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        assert package_version.stdout.strip() == f"Hyperflow {__version__}"

        console_version = run_checked([str(cli), "--version"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        assert console_version.stdout.strip() == f"Hyperflow {__version__}"

        run = run_checked([str(py), "-m", "hyperflow.interface.cli", "🌈💎🔥🧠🔀⚡ sdist smoke"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        payload = json.loads(run.stdout)
        assert payload["run_id"]
        assert payload["contract"]["schema"] == "hyperflow/edde-contract/v1"

        package_run = run_checked([str(py), "-m", "hyperflow", "🌈💎🔥🧠🔀⚡ sdist smoke"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
        package_payload = json.loads(package_run.stdout)
        assert package_payload["run_id"]
        assert package_payload["contract"]["schema"] == "hyperflow/edde-contract/v1"

        console_run = run_checked([str(cli), "🌈💎🔥🧠🔀⚡ sdist smoke"], cwd=outside_dir, env=env, timeout=LIGHT_TIMEOUT_SECONDS)
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
