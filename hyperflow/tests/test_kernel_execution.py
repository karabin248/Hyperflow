from __future__ import annotations

from types import SimpleNamespace

from hyperflow.engine.execution_bundle import ExecutionBundle
from hyperflow.engine.kernel_execution import _run_step_with_retry, format_output_unified, select_executor
from hyperflow.engine.run_request import AgentTaskRequest, AgentTaskSpec, WorkflowStepRequest, WorkflowStepSpec
from hyperflow.schemas.command_schema import CommandObject


def test_select_executor_is_single_request_type_branch_point() -> None:
    command = CommandObject(raw_input="🌈💎🔥🧠🔀⚡ test")
    assert select_executor(command) == "edde"

    step_request = WorkflowStepRequest(
        raw_input="step",
        intent="build",
        mode="analysis",
        step_spec=WorkflowStepSpec(
            workflow_id="wf",
            node_id="n1",
            node_type="tool",
            ref="tool.ref",
            parent_run_id="run-1",
            idempotency_key="idem-1",
        ),
    )
    assert select_executor(step_request) == "workflow_step"

    task_request = AgentTaskRequest(
        raw_input="task",
        task_spec=AgentTaskSpec(
            plan_id="plan-1",
            task_id="task-1",
            role_id="reasoning-worker",
            parent_run_id="run-1",
            idempotency_key="idem-2",
        ),
    )
    assert select_executor(task_request) == "agent_task"


def test_format_output_unified_uses_kernel_final_report_status() -> None:
    state = SimpleNamespace(run_id="run-1", plan=["fallback"])
    bundle = ExecutionBundle(
        summary="ok",
        confidence=0.8,
        observer_status="OK",
        next_step="done",
        execution_path="agent_task",
        step_ref="reasoning-worker",
    )
    report = SimpleNamespace(observer_status="WARN")

    payload = format_output_unified(CommandObject(raw_input="x"), state, bundle, report)

    assert payload["run_id"] == "run-1"
    assert payload["observer_status"] == "WARN"
    assert payload["execution_path"] == "agent_task"


def test_run_step_with_retry_respects_retry_policy_and_run_id() -> None:
    events = []

    def _emit(run_id, event_type, payload):
        events.append((run_id, event_type, payload))

    state = SimpleNamespace(run_id="run-constant")
    request = WorkflowStepRequest(
        raw_input="step",
        intent="build",
        mode="analysis",
        step_spec=WorkflowStepSpec(
            workflow_id="wf",
            node_id="extract",
            node_type="approval",
            ref="approval",
            parent_run_id="run-constant",
            idempotency_key="idem",
            retry_policy={"max_attempts": 2},
            input_payload={"approved": True},
        ),
    )

    bundle = _run_step_with_retry(request, state, emit_event=_emit)

    assert bundle.execution_path.startswith("workflow_step")
    assert all(run_id == "run-constant" for run_id, _, _ in events)


def test_run_step_with_retry_returns_fallback_for_missing_step_spec() -> None:
    state = SimpleNamespace(run_id="run-1")
    request = WorkflowStepRequest(raw_input="step", intent="build", mode="analysis", step_spec=None)

    bundle = _run_step_with_retry(request, state, emit_event=lambda *_: None)

    assert bundle.observer_status == "FALLBACK"
    assert bundle.error_code == "STEP_SPEC_MISSING"
    assert bundle.execution_path == "workflow_step"


def test_run_step_with_retry_handles_invalid_retry_policy_value() -> None:
    events = []

    def _emit(run_id, event_type, payload):
        events.append((run_id, event_type, payload))

    state = SimpleNamespace(run_id="run-1")
    request = AgentTaskRequest(
        raw_input="task",
        task_spec=AgentTaskSpec(
            plan_id="plan-1",
            task_id="task-1",
            role_id="missing-worker",
            parent_run_id="run-1",
            idempotency_key="idempotency-1",
            retry_policy={"max_attempts": "not-a-number"},
        ),
    )

    bundle = _run_step_with_retry(request, state, emit_event=_emit)

    assert bundle.execution_path.endswith(":attempt_1")
    assert events == []
