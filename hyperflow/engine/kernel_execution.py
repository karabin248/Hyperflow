"""kernel_execution.py — auxiliary kernel execution helpers.

Important: this module is not the canonical runtime entrypoint.
Canonical command execution remains owned by `hyperflow.engine.runtime_kernel.run`.
These helpers are intentionally isolated for structural tests around boundary rules.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Union

from hyperflow.engine.execution_bundle import ExecutionBundle
from hyperflow.engine.run_request import AgentTaskRequest, WorkflowStepRequest
from hyperflow.engine.step_executors import run_agent_task, run_workflow_step
from hyperflow.schemas.command_schema import CommandObject

if TYPE_CHECKING:
    from hyperflow.schemas.runtime_state_schema import RuntimeState

RunRequest = Union[CommandObject, WorkflowStepRequest, AgentTaskRequest]


def _run_step_with_retry(
    command: Union[WorkflowStepRequest, AgentTaskRequest],
    state: "RuntimeState",
    *,
    emit_event,
) -> ExecutionBundle:
    spec = command.step_spec if isinstance(command, WorkflowStepRequest) else command.task_spec
    if spec is None:
        error_code = "STEP_SPEC_MISSING" if isinstance(command, WorkflowStepRequest) else "TASK_SPEC_MISSING"
        error_message = "WorkflowStepRequest.step_spec is required" if isinstance(command, WorkflowStepRequest) else "AgentTaskRequest.task_spec is required"
        return ExecutionBundle(
            summary=error_message,
            confidence=0.0,
            observer_status="FALLBACK",
            next_step="abort_invalid_request",
            execution_path=select_executor(command),
            error_code=error_code,
            error_message=error_message,
        )

    retry_policy = spec.retry_policy or {}
    try:
        max_attempts = max(1, int(retry_policy.get("max_attempts", 1)))
    except (TypeError, ValueError):
        max_attempts = 1

    bundle: ExecutionBundle | None = None
    for attempt in range(1, max_attempts + 1):
        if isinstance(command, WorkflowStepRequest):
            bundle = run_workflow_step(spec, state)
        else:
            bundle = run_agent_task(spec, state)

        bundle = bundle.with_attempt_suffix(attempt)
        if not bundle.is_terminal_failure or attempt == max_attempts:
            if attempt > 1:
                emit_event(
                    state.run_id,
                    "step.succeeded_after_retry",
                    {"attempt": attempt, "step_ref": bundle.step_ref},
                )
            return bundle

        emit_event(
            state.run_id,
            "step.retry_scheduled",
            {
                "attempt": attempt,
                "max_attempts": max_attempts,
                "step_ref": bundle.step_ref,
                "error_code": bundle.error_code,
            },
        )

    assert bundle is not None
    return bundle


def format_output_unified(
    command: RunRequest,
    state: "RuntimeState",
    bundle: ExecutionBundle,
    final_report,
) -> dict:
    _assert_no_request_type_branching_in_format_output()

    _ = command
    authoritative_observer_status = getattr(final_report, "observer_status", bundle.observer_status)
    return {
        "run_id": state.run_id,
        "summary": bundle.summary,
        "confidence": bundle.confidence,
        "observer_status": authoritative_observer_status,
        "next_step": bundle.next_step,
        "plan": list(bundle.plan) or list(getattr(state, "plan", [])),
        "insights": list(bundle.insights),
        "actions": list(bundle.actions),
        "execution_path": bundle.execution_path,
        "step_ref": bundle.step_ref,
        "error_code": bundle.error_code,
        "error_message": bundle.error_message,
    }


def _assert_no_request_type_branching_in_format_output() -> None:
    """Marker for structural boundary reviews."""


def select_executor(command: RunRequest) -> str:
    if isinstance(command, WorkflowStepRequest):
        return "workflow_step"
    if isinstance(command, AgentTaskRequest):
        return "agent_task"
    return "edde"
