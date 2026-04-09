"""step_executors.py — Thin adapters between kernel and dispatch layer."""

from __future__ import annotations

from typing import TYPE_CHECKING

from hyperflow.engine.dispatch import _dispatch_node, _invoke_role_worker, _pure_dispatch_scope
from hyperflow.engine.execution_bundle import ExecutionBundle
from hyperflow.engine.run_request import AgentTaskSpec, WorkflowStepSpec

if TYPE_CHECKING:
    from hyperflow.schemas.runtime_state_schema import RuntimeState


def run_workflow_step(spec: WorkflowStepSpec, state: "RuntimeState") -> ExecutionBundle:
    _ = state
    _assert_no_retry_in_spec_was_read_here()
    try:
        with _pure_dispatch_scope("run_workflow_step._dispatch_node"):
            raw_output = _dispatch_node(spec)
    except Exception as exc:
        return ExecutionBundle(
            summary=f"Node {spec.node_id!r} ({spec.node_type}) failed via {spec.ref!r}: {exc}",
            confidence=0.0,
            observer_status="FALLBACK",
            next_step="handle_step_failure",
            execution_path="workflow_step",
            step_ref=spec.ref,
            input_payload=spec.input_payload,
            error_code="STEP_EXECUTION_ERROR",
            error_message=str(exc),
        )

    return ExecutionBundle(
        summary=_extract_summary(raw_output, fallback=f"Node {spec.node_id!r} completed via {spec.ref!r}"),
        confidence=_extract_confidence(raw_output, fallback=1.0),
        observer_status=_extract_observer_status(raw_output, fallback="OK"),
        next_step=_extract_next_step(raw_output, fallback=""),
        execution_path="workflow_step",
        step_ref=spec.ref,
        input_payload=spec.input_payload,
        output_payload=raw_output,
    )


def run_agent_task(spec: AgentTaskSpec, state: "RuntimeState") -> ExecutionBundle:
    _ = state
    try:
        with _pure_dispatch_scope("run_agent_task._invoke_role_worker"):
            raw_output = _invoke_role_worker(spec)
    except Exception as exc:
        return ExecutionBundle(
            summary=f"Task {spec.task_id!r} (role {spec.role_id!r}) failed: {exc}",
            confidence=0.0,
            observer_status="FALLBACK",
            next_step="handle_task_failure",
            execution_path="agent_task",
            step_ref=spec.role_id,
            input_payload=spec.input_payload,
            error_code="TASK_EXECUTION_ERROR",
            error_message=str(exc),
        )

    return ExecutionBundle(
        summary=_extract_summary(raw_output, fallback=f"Task {spec.task_id!r} completed"),
        confidence=_extract_confidence(raw_output, fallback=1.0),
        observer_status=_extract_observer_status(raw_output, fallback="OK"),
        next_step=_extract_next_step(raw_output, fallback=""),
        execution_path="agent_task",
        step_ref=spec.role_id,
        input_payload=spec.input_payload,
        output_payload=raw_output,
    )


def _extract_summary(raw: object, *, fallback: str) -> str:
    if isinstance(raw, dict):
        v = raw.get("summary") or raw.get("result") or raw.get("output")
        if isinstance(v, str) and v:
            return v
    return fallback


def _extract_confidence(raw: object, *, fallback: float) -> float:
    if isinstance(raw, dict):
        v = raw.get("confidence")
        try:
            f = float(v)
            if 0.0 <= f <= 1.0:
                return f
        except (TypeError, ValueError):
            pass
    return fallback


def _extract_observer_status(raw: object, *, fallback: str) -> str:
    if isinstance(raw, dict):
        v = raw.get("observer_status")
        if v in {"OK", "WARN", "FALLBACK"}:
            return v
    return fallback


def _extract_next_step(raw: object, *, fallback: str) -> str:
    if isinstance(raw, dict):
        v = raw.get("next_step")
        if isinstance(v, str):
            return v
    return fallback


def _assert_no_retry_in_spec_was_read_here() -> None:
    """Marker function for reviewer boundary checks."""
