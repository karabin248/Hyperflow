"""run_request.py — Canonical input contract for runtime_kernel.run()."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Union

9
@dataclass
class WorkflowStepSpec:
    workflow_id: str
    node_id: str
    node_type: Literal["tool", "worker", "agent", "approval"]
    ref: str
    parent_run_id: str
    idempotency_key: str
    retry_policy: dict[str, Any] = field(default_factory=dict)
    input_payload: Any = None


@dataclass
class AgentTaskSpec:
    plan_id: str
    task_id: str
    role_id: str
    parent_run_id: str
    idempotency_key: str
    retry_policy: dict[str, Any] = field(default_factory=dict)
    input_payload: Any = None


@dataclass
class WorkflowStepRequest:
    raw_input: str
    intent: str
    mode: str
    output_type: str = "result"
    intensity: int = 3
    tokens: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    action_routes: list[dict] = field(default_factory=list)
    step_spec: WorkflowStepSpec | None = None


@dataclass
class AgentTaskRequest:
    raw_input: str
    intent: str = "delegate"
    mode: str = "agent"
    output_type: str = "result"
    intensity: int = 3
    tokens: list[str] = field(default_factory=list)
    operations: list[str] = field(default_factory=list)
    action_routes: list[dict] = field(default_factory=list)
    task_spec: AgentTaskSpec | None = None


RunRequest = Union["CommandObject", WorkflowStepRequest, AgentTaskRequest]
