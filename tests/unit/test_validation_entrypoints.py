from __future__ import annotations

from pathlib import Path


def _read(path: str) -> str:
    root = Path(__file__).resolve().parents[2]
    return (root / path).read_text(encoding="utf-8")


def test_make_test_uses_shared_regression_entrypoint() -> None:
    makefile = _read("Makefile")
    assert "test:\n\tbash scripts/test_suite.sh\n" in makefile
    assert "pytest -q" not in makefile.split("test:", 1)[1].split("clean:", 1)[0]


def test_repo_gate_uses_shared_regression_entrypoint_without_pip_upgrade() -> None:
    script = _read("scripts/check_everything.sh")
    assert "bash scripts/test_suite.sh" in script
    assert "install --upgrade pip" not in script


def test_shared_test_suite_excludes_packaging_smoke() -> None:
    script = _read("scripts/test_suite.sh")
    assert "test_built_sdist_smoke.py" in script
    assert "test_built_wheel_smoke.py" in script


def test_pytest_config_excludes_generated_artifact_dirs() -> None:
    pytest_ini = _read("pytest.ini")
    assert "norecursedirs = build dist wheelhouse .pytest_cache *.egg-info" in pytest_ini
