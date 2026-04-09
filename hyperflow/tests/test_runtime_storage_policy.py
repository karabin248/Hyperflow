from __future__ import annotations

from pathlib import Path

from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_paths import get_agent_run_trace_file, get_checkpoint_dir, get_knowledge_file, get_storage_root, get_trace_file


def test_default_storage_targets_cwd_outside_repo(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert get_storage_root() == tmp_path / "storage"


def test_default_storage_redirects_when_cwd_is_repo_root(tmp_path: Path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(repo_root)
    assert get_storage_root() == tmp_path / ".hyperflow" / "storage"


def test_runtime_run_from_repo_root_does_not_dirty_repo_storage(tmp_path: Path, monkeypatch) -> None:
    repo_root = Path(__file__).resolve().parents[2]
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.chdir(repo_root)

    command = build_command("🌈💎🔥🧠🔀⚡ Task: validate repo-root storage policy")
    result = run(command)

    repo_storage_files = [
        path.relative_to(repo_root).as_posix()
        for path in (repo_root / "storage").rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]
    assert repo_storage_files == []
    assert get_trace_file().exists()
    assert get_knowledge_file().exists()
    assert (get_checkpoint_dir() / f"{result.run_id}.json").exists()


def test_agent_runtime_trace_storage_follows_storage_root(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert get_agent_run_trace_file() == tmp_path / "storage" / "agent_runs.jsonl"
