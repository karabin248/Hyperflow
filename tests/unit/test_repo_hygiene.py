import os
import subprocess
from pathlib import Path


def _session_start_cutoff() -> float:
    raw = os.environ.get('HYPERFLOW_TEST_SESSION_START')
    try:
        return float(raw) if raw else 0.0
    except ValueError:
        return 0.0


def _is_allowed_test_session_artifact(path: Path, root: Path) -> bool:
    rel = path.relative_to(root).as_posix()
    allowed_prefixes = (
        'hyperflow/tests/__pycache__/',
        'tests/__pycache__/',
    )
    return rel == 'hyperflow/tests/__pycache__' or rel == 'tests/__pycache__' or rel.startswith(allowed_prefixes)


def _is_preexisting_generated_artifact(path: Path, root: Path) -> bool:
    if _is_allowed_test_session_artifact(path, root):
        return False
    return path.stat().st_mtime <= _session_start_cutoff()


def _tracked_repo_paths(root: Path) -> set[str]:
    try:
        proc = subprocess.run(
            ["git", "ls-files", "-z"],
            cwd=root,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError):
        return set()
    return {entry for entry in proc.stdout.decode("utf-8").split("\x00") if entry}


def test_legacy_root_checkpoint_history_removed():
    root = Path(__file__).resolve().parents[2]
    assert not (root / "checkpoint_history.json").exists()


def test_legacy_commands_doc_archived():
    root = Path(__file__).resolve().parents[2]
    assert not (root / "hyperflow" / "commands" / "commands.md").exists()
    assert not (root / "archive").exists()


def test_canonical_runtime_surface_exists():
    root = Path(__file__).resolve().parents[2]
    assert (root / "core" / "CANONICAL_RUNTIME_SURFACE.md").exists()


def test_repo_root_storage_payloads_not_committed():
    root = Path(__file__).resolve().parents[2]
    storage_root = root / "storage"
    committed_payloads = [
        path.relative_to(root).as_posix()
        for path in storage_root.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    assert committed_payloads == []


def test_generated_build_artifacts_not_committed():
    root = Path(__file__).resolve().parents[2]
    assert not (root / "build").exists()
    assert not (root / "dist").exists()
    assert not (root / "wheelhouse").exists()
    assert not (root / ".pytest_cache").exists()


def test_generated_artifacts_are_gitignored():
    root = Path(__file__).resolve().parents[2]
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    assert "build/" in gitignore
    assert "dist/" in gitignore
    assert "wheelhouse/" in gitignore
    assert ".pytest_cache/" in gitignore
    assert "*.egg-info/" in gitignore
    assert "hyperflow.egg-info/" in gitignore


def test_python_cache_dirs_not_committed():
    root = Path(__file__).resolve().parents[2]
    tracked = _tracked_repo_paths(root)
    committed = sorted(path for path in tracked if "/__pycache__/" in f"/{path}/" or path.endswith("/__pycache__"))
    assert committed == []


def test_compiled_python_artifacts_not_committed():
    root = Path(__file__).resolve().parents[2]
    tracked = _tracked_repo_paths(root)
    committed = sorted(path for path in tracked if path.endswith(".pyc") or path.endswith(".pyo"))
    assert committed == []


def test_egg_info_not_committed():
    root = Path(__file__).resolve().parents[2]
    tracked = _tracked_repo_paths(root)
    committed = sorted(path for path in tracked if path.endswith(".egg-info") or ".egg-info/" in path)
    assert committed == []


def test_source_zip_artifacts_not_committed():
    root = Path(__file__).resolve().parents[2]
    assert not any(root.glob("hyperflow-v*-source.zip"))
    assert not (root / "hyperflow-source.zip").exists()


def test_source_zip_artifacts_are_gitignored():
    root = Path(__file__).resolve().parents[2]
    gitignore = (root / ".gitignore").read_text(encoding="utf-8")
    assert "hyperflow-source.zip" in gitignore
    assert "hyperflow-v*-source.zip" in gitignore
