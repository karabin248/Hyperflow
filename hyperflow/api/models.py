from __future__ import annotations

from typing import Any

try:
    from pydantic import BaseModel, Field
except ModuleNotFoundError:  # pragma: no cover - optional dependency bridge
    BaseModel = object  # type: ignore[assignment]
    Field = lambda default=None, **_kwargs: default  # type: ignore[misc]


class RunRequest(BaseModel):
    prompt: str = Field(..., description="Raw Hyperflow prompt or control string")


class RunResponse(BaseModel):
    run_id: str
    intent: str
    mode: str
    output_type: str
    result: dict[str, Any]
    contract: dict[str, Any]


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class AgentInfo(BaseModel):
    id: str
    role: str
    capability: str


class AgentListResponse(BaseModel):
    items: list[AgentInfo]


class WorkerInfo(BaseModel):
    id: str
    role: str
    capability: str
    description: str
    execution: str
    integrated_with_runtime: bool


class WorkerListResponse(BaseModel):
    items: list[WorkerInfo]


class WorkflowInfo(BaseModel):
    id: str
    name: str
    description: str
    intent: str
    mode: str


class WorkflowListResponse(BaseModel):
    items: list[WorkflowInfo]


class WorkflowRunRequest(BaseModel):
    input_payload: dict[str, Any] = Field(default_factory=dict)
    approvals: dict[str, bool] = Field(default_factory=dict)


class WorkflowRunResponse(BaseModel):
    run_id: str
    status: str
    output: Any
    node_results: list[dict[str, Any]] = Field(default_factory=list)
    waiting_on_node: str | None = None


class AgentRunRequest(BaseModel):
    input_payload: dict[str, Any] = Field(default_factory=dict)


class AgentRunResponse(BaseModel):
    run_id: str
    output: dict[str, Any]


class CheckpointSummary(BaseModel):
    checkpoint_id: str = ""
    run_id: str = ""
    file_name: str = ""
    file_path: str = ""
    generated_at: str = ""
    version: str = ""
    status: str = ""
    development_phase: str = ""
    dominant_work_style: str = ""
    dominant_intent: str = ""
    dominant_mode: str = ""
    core_operating_kernel: list[str] = Field(default_factory=list)
    satellite_modes: list[str] = Field(default_factory=list)


class CheckpointListResponse(BaseModel):
    items: list[CheckpointSummary]


class TraceListResponse(BaseModel):
    items: list[dict[str, Any]]


class WorkflowSubmitResponse(BaseModel):
    ticket_id: str
    workflow_id: str
    status: str
    queued_at: str
    run_id: str | None = None
    result: dict[str, Any] | None = None


class WorkflowQueueListResponse(BaseModel):
    items: list[dict[str, Any]]
