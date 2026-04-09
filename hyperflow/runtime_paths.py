from __future__ import annotations

import os
from pathlib import Path


def _repo_root_markers(root: Path) -> bool:
    return (root / "pyproject.toml").exists() and (root / "hyperflow").is_dir() and (root / "README.md").exists()


def current_repo_root() -> Path | None:
    cwd = Path.cwd()
    return cwd if _repo_root_markers(cwd) else None


def get_storage_root() -> Path:
    explicit = os.environ.get("HYPERFLOW_STORAGE_DIR", "").strip()
    if explicit:
        return Path(explicit).expanduser()

    repo_root = current_repo_root()
    if repo_root is not None:
        state_home = os.environ.get("HYPERFLOW_STATE_HOME", "").strip()
        if state_home:
            return Path(state_home).expanduser() / "storage"
        return Path.home() / ".hyperflow" / "storage"

    return Path.cwd() / "storage"


def get_trace_file() -> Path:
    return get_storage_root() / "traces.jsonl"


def get_graph_file() -> Path:
    return get_storage_root() / "graph_memory.json"


def get_knowledge_file() -> Path:
    return get_storage_root() / "knowledge_store.jsonl"


def get_checkpoint_dir() -> Path:
    return get_storage_root() / "checkpoints"


def get_checkpoint_file(checkpoint_id: str) -> Path:
    return get_checkpoint_dir() / f"{checkpoint_id}.json"


def get_agent_run_trace_file() -> Path:
    return get_storage_root() / "agent_runs.jsonl"


def get_agent_promotion_review_dir() -> Path:
    return get_storage_root() / "agent_reviews"


def get_distributed_store_file() -> Path:
    return get_storage_root() / "distributed_state.json"
