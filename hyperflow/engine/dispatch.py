"""dispatch.py — Pure, framework-free dispatch boundaries for step executors."""

from __future__ import annotations

import threading
from contextlib import contextmanager
from typing import Any, Generator

from hyperflow.engine import registry as engine_registry
from hyperflow.engine.execution_context import ToolExecutionContext, WorkerExecutionContext
from hyperflow.engine.registry import resolve_tool_handler, resolve_worker_handler
from hyperflow.engine.run_request import AgentTaskSpec, WorkflowStepSpec

_dispatch_active = threading.local()


class DispatchPurityViolation(RuntimeError):
    """Raised when a pure-dispatch boundary is violated."""


@contextmanager
def _pure_dispatch_scope(label: str) -> Generator[None, None, None]:
    previous = getattr(_dispatch_active, "label", None)
    _dispatch_active.label = label
    try:
        yield
    finally:
        _dispatch_active.label = previous


def assert_pure_dispatch_context(operation: str) -> None:
    label = getattr(_dispatch_active, "label", None)
    if label is not None:
        raise DispatchPurityViolation(
            f"Prohibited operation {operation!r} attempted inside pure dispatch scope {label!r}."
        )


def _dispatch_node(spec: WorkflowStepSpec) -> Any:
    if spec.node_type == "tool":
        return _invoke_tool(
            spec.ref,
            spec.input_payload,
            spec.idempotency_key,
            run_id=spec.parent_run_id,
            workflow_id=spec.workflow_id,
            node_id=spec.node_id,
        )
    if spec.node_type == "worker":
        return _invoke_worker(
            spec.ref,
            spec.input_payload,
            spec.idempotency_key,
            run_id=spec.parent_run_id,
            workflow_id=spec.workflow_id,
            node_id=spec.node_id,
        )
    if spec.node_type == "approval":
        approved = bool((spec.input_payload or {}).get("approved", False))
        if not approved:
            raise ValueError(f"Approval node {spec.node_id!r} reached dispatch without approval.")
        return {"approved": True, "node_id": spec.node_id}
    raise ValueError(
        f"Unsupported node_type {spec.node_type!r} in _dispatch_node. "
        "Valid types: 'tool', 'worker', 'approval'. Agent execution must be lowered to AgentTaskSpec before dispatch."
    )


def _invoke_role_worker(spec: AgentTaskSpec) -> dict[str, Any]:
    return _invoke_worker(
        spec.role_id,
        spec.input_payload,
        spec.idempotency_key,
        run_id=spec.parent_run_id,
        workflow_id=spec.plan_id,
        node_id=spec.task_id,
    )


def _invoke_tool(
    tool_ref: str,
    input_payload: Any,
    idempotency_key: str,
    *,
    run_id: str | None = None,
    workflow_id: str | None = None,
    node_id: str | None = None,
) -> Any:
    try:
        handler = resolve_tool_handler(tool_ref)
    except ValueError:
        engine_registry.seed_default_handlers()
        handler = resolve_tool_handler(tool_ref)

    ctx = ToolExecutionContext(
        run_id=run_id or f"dispatch-tool-{idempotency_key}",
        node_id=node_id or tool_ref,
        workflow_id=workflow_id or "dispatch",
        idempotency_key=idempotency_key,
    )
    return handler(input_payload, ctx)


def _invoke_worker(
    worker_ref: str,
    input_payload: Any,
    idempotency_key: str,
    *,
    run_id: str | None = None,
    workflow_id: str | None = None,
    node_id: str | None = None,
) -> Any:
    try:
        handler = resolve_worker_handler(worker_ref)
    except ValueError:
        engine_registry.seed_default_handlers()
        handler = resolve_worker_handler(worker_ref)

    ctx = WorkerExecutionContext(
        run_id=run_id or f"dispatch-worker-{idempotency_key}",
        node_id=node_id or worker_ref,
        workflow_id=workflow_id or "dispatch",
        idempotency_key=idempotency_key,
    )
    return handler(input_payload, ctx)


__all__ = [
    "DispatchPurityViolation",
    "_dispatch_node",
    "_invoke_role_worker",
    "_invoke_tool",
    "_invoke_worker",
    "_pure_dispatch_scope",
    "assert_pure_dispatch_context",
]
