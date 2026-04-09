"""test_engine_dispatch.py — Dispatch resolves handlers from engine registry directly.

After the HB-2 fix, dispatch.py no longer calls _get_runtime_framework() or
create_operational_framework().  These tests verify that:
- _dispatch_node routes tool/worker nodes through the engine registry
- _invoke_role_worker routes through the engine registry
- Handler context fields (run_id, workflow_id, node_id, idempotency_key) are
  correctly forwarded to the handler
"""

from __future__ import annotations

from hyperflow.engine import dispatch, registry as engine_registry
from hyperflow.engine.run_request import AgentTaskSpec, WorkflowStepSpec


def _make_tool_spec(
    *,
    tool_ref: str = "data.ingest_records",
    input_payload: dict | None = None,
    run_id: str = "run-123",
    workflow_id: str = "wf-1",
    node_id: str = "node-ingest",
    idempotency_key: str = "wf-1:node-ingest:run-123",
) -> WorkflowStepSpec:
    return WorkflowStepSpec(
        workflow_id=workflow_id,
        node_id=node_id,
        node_type="tool",
        ref=tool_ref,
        parent_run_id=run_id,
        idempotency_key=idempotency_key,
        input_payload=input_payload or {"path": "sample.csv", "source_type": "csv"},
    )


def _make_worker_spec(
    *,
    worker_ref: str = "reasoning-worker",
    input_payload: dict | None = None,
    run_id: str = "run-456",
    workflow_id: str = "wf-2",
    node_id: str = "node-reason",
    idempotency_key: str = "wf-2:node-reason:run-456",
) -> WorkflowStepSpec:
    return WorkflowStepSpec(
        workflow_id=workflow_id,
        node_id=node_id,
        node_type="worker",
        ref=worker_ref,
        parent_run_id=run_id,
        idempotency_key=idempotency_key,
        input_payload=input_payload or {"objective": "summarize"},
    )


def test_dispatch_node_tool_resolves_from_engine_registry(monkeypatch) -> None:
    """_dispatch_node for a tool node must resolve the handler from engine registry."""
    calls: list[tuple] = []

    def fake_tool_handler(payload, ctx):
        calls.append(("tool", payload, ctx))
        return {"tool": "data.ingest_records", "ok": True}

    monkeypatch.setitem(engine_registry._TOOL_HANDLERS, "data.ingest_records", fake_tool_handler)
    spec = _make_tool_spec()
    result = dispatch._dispatch_node(spec)

    assert result == {"tool": "data.ingest_records", "ok": True}
    assert len(calls) == 1
    _, payload, ctx = calls[0]
    assert payload == spec.input_payload
    assert ctx.run_id == "run-123"
    assert ctx.workflow_id == "wf-1"
    assert ctx.node_id == "node-ingest"
    assert ctx.idempotency_key == "wf-1:node-ingest:run-123"


def test_dispatch_node_worker_resolves_from_engine_registry(monkeypatch) -> None:
    """_dispatch_node for a worker node must resolve the handler from engine registry."""
    calls: list[tuple] = []

    def fake_worker_handler(payload, ctx):
        calls.append(("worker", payload, ctx))
        return {"worker": "reasoning-worker", "ok": True}

    monkeypatch.setitem(engine_registry._WORKER_HANDLERS, "reasoning-worker", fake_worker_handler)
    spec = _make_worker_spec()
    result = dispatch._dispatch_node(spec)

    assert result == {"worker": "reasoning-worker", "ok": True}
    assert len(calls) == 1
    _, payload, ctx = calls[0]
    assert payload == spec.input_payload
    assert ctx.run_id == "run-456"
    assert ctx.workflow_id == "wf-2"
    assert ctx.node_id == "node-reason"
    assert ctx.idempotency_key == "wf-2:node-reason:run-456"


def test_invoke_role_worker_routes_through_engine_registry(monkeypatch) -> None:
    """_invoke_role_worker must resolve through engine registry, not framework."""
    calls: list[tuple] = []

    def fake_report_handler(payload, ctx):
        calls.append(("worker", payload, ctx))
        return {"worker": "reporting-worker", "ok": True}

    monkeypatch.setitem(engine_registry._WORKER_HANDLERS, "reporting-worker", fake_report_handler)

    spec = AgentTaskSpec(
        plan_id="plan-1",
        task_id="task-a",
        role_id="reporting-worker",
        parent_run_id="agent-run-9",
        idempotency_key="task-a:reporting-worker",
        input_payload={"draft": "hello"},
    )

    result = dispatch._invoke_role_worker(spec)

    assert result == {"worker": "reporting-worker", "ok": True}
    assert len(calls) == 1
    _, payload, ctx = calls[0]
    assert payload == spec.input_payload
    assert ctx.run_id == "agent-run-9"
    assert ctx.workflow_id == "plan-1"
    assert ctx.node_id == "task-a"
    assert ctx.idempotency_key == "task-a:reporting-worker"


def test_dispatch_does_not_reference_framework_runtime(monkeypatch) -> None:
    """dispatch.py must not import or reference hyperflow.framework.runtime."""
    import importlib.util
    import inspect
    import hyperflow.engine.dispatch as dispatch_mod

    source = inspect.getsource(dispatch_mod)
    assert "framework.runtime" not in source
    assert "create_operational_framework" not in source
    assert "_get_runtime_framework" not in source
    assert "_get_operational_framework" not in source


def test_registry_does_not_reference_framework_runtime() -> None:
    """engine/registry.py must not import hyperflow.framework.runtime."""
    import inspect
    import hyperflow.engine.registry as reg_mod

    source = inspect.getsource(reg_mod)
    assert "create_operational_framework" not in source
    assert "framework.runtime" not in source
