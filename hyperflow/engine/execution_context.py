from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ToolExecutionContext:
    run_id: str
    node_id: str
    workflow_id: str
    idempotency_key: str = ""


@dataclass(frozen=True)
class WorkerExecutionContext:
    run_id: str
    node_id: str
    workflow_id: str
    idempotency_key: str = ""
