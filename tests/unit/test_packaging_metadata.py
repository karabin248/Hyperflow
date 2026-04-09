from __future__ import annotations

import tomllib
from pathlib import Path

from hyperflow.version import get_version

REPO_ROOT = Path(__file__).resolve().parents[2]
ROOT = REPO_ROOT
RELEASE_NOTES = REPO_ROOT / f"RELEASE_NOTES_v{get_version()}.md"


def test_pyproject_declares_dynamic_version_console_script_and_api_extra() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = data["project"]

    assert project["dynamic"] == ["version"]
    assert data["tool"]["setuptools"]["dynamic"]["version"]["attr"] == "hyperflow.version.__version__"
    assert project["scripts"]["hyperflow"] == "hyperflow.interface.cli:main"

    extras = project["optional-dependencies"]
    assert "api" in extras
    assert any(dep.startswith("fastapi>=") for dep in extras["api"])
    assert any(dep.startswith("uvicorn>=") for dep in extras["api"])
    assert "test" in extras
    assert any(dep.startswith("pytest>=") for dep in extras["test"])


def test_pyproject_includes_packaged_runtime_configs() -> None:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    package_data = data["tool"]["setuptools"]["package-data"]

    assert "hyperflow" in package_data
    assert "configs/*.json" in package_data["hyperflow"]


def test_packaged_runtime_config_files_exist() -> None:
    packaged_configs = ROOT / "hyperflow" / "configs"

    assert (packaged_configs / "edde-core.json").exists()
    assert (packaged_configs / "mps-regulator.json").exists()
    assert (packaged_configs / "system-shell.json").exists()
    assert (packaged_configs / "canonical-emoji-library.json").exists()
    assert (packaged_configs / "emoji-action-router.json").exists()


def test_api_factory_docs_are_consistent() -> None:
    expected = "uvicorn hyperflow.api.edde_api:create_app --factory"
    for doc_path in [
        REPO_ROOT / "README.md",
        RELEASE_NOTES,
        REPO_ROOT / "core/RC_RELEASE_CHECKLIST.md",
    ]:
        content = doc_path.read_text(encoding="utf-8")
        assert expected in content
        assert "uvicorn hyperflow.api.edde_api:app --factory" not in content


def test_runtime_version_constant_matches_release_line() -> None:
    from hyperflow.version import __version__, get_version

    assert __version__ == get_version()


def test_operator_docs_include_package_module_entrypoint() -> None:
    expected_commands = [
        "python -m hyperflow --version",
        'python -m hyperflow "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty',
    ]
    for doc_path in [
        REPO_ROOT / "README.md",
        RELEASE_NOTES,
        REPO_ROOT / "core/RC_RELEASE_CHECKLIST.md",
    ]:
        content = doc_path.read_text(encoding="utf-8")
        for command in expected_commands:
            assert command in content


def test_operator_docs_include_versioned_source_zip_default() -> None:
    version = get_version()
    expected_lines = [
        "python scripts/make_source_zip.py",
        f"hyperflow-v{version}-source.zip",
    ]
    archive_root = f"hyperflow-v{version}/"
    for doc_path in [
        REPO_ROOT / "README.md",
        RELEASE_NOTES,
        REPO_ROOT / "core/RC_RELEASE_CHECKLIST.md",
    ]:
        content = doc_path.read_text(encoding="utf-8")
        for line in expected_lines:
            assert line in content
        assert archive_root in content
        assert "hyperflow-source.zip" not in content
