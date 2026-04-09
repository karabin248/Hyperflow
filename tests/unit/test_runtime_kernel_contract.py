"""Contract test: runtime_kernel.run() must return a plain sync object, never an awaitable.

This test exists to prevent regression of the _SyncAsyncResult shim pattern.
If this test fails it means someone re-introduced an async wrapper inside the
canonical runtime kernel, which violates the baseline contract.
"""
import inspect

from hyperflow.engine import runtime_kernel
from hyperflow.schemas.command_schema import CommandObject


def test_runtime_kernel_run_returns_plain_result(monkeypatch):
    """run() must return a plain synchronous result object, not an awaitable."""

    class DummyResult:
        summary = "ok"
        observer_status = "OK"
        observer_contract = None
        edde_contract = None

    class DummyState:
        run_id = "run-test-1"
        observer_status = "OK"
        mps_level = "default"
        plan = None

    class DummyReport:
        observer_status = "OK"

    monkeypatch.setattr(runtime_kernel, "init_runtime_state", lambda c: DummyState())
    monkeypatch.setattr(runtime_kernel, "pre_run_check", lambda c: DummyReport())
    monkeypatch.setattr(runtime_kernel, "resolve_mps_level", lambda c: "default")
    monkeypatch.setattr(runtime_kernel, "apply_mps_profile", lambda s: s)
    monkeypatch.setattr(runtime_kernel, "build_plan", lambda c, s: {"steps": []})
    monkeypatch.setattr(runtime_kernel, "run_edde", lambda c, s: {"bundle": "ok"})
    monkeypatch.setattr(runtime_kernel, "final_check", lambda c, s, b: DummyReport())
    monkeypatch.setattr(runtime_kernel, "apply_fallback", lambda c, s, b: (s, b))
    monkeypatch.setattr(runtime_kernel, "format_output", lambda c, s, b, r: DummyResult())
    monkeypatch.setattr(runtime_kernel, "build_observer_contract", lambda report: {"status": "ok"})
    monkeypatch.setattr(runtime_kernel, "build_edde_contract", lambda *a, **kw: {"version": "1"})
    monkeypatch.setattr(runtime_kernel, "validate_edde_contract", lambda c: None)
    monkeypatch.setattr(runtime_kernel, "build_trace_record", lambda *a, **kw: {"trace": "ok"})
    monkeypatch.setattr(runtime_kernel, "append_trace", lambda *a, **kw: None)
    monkeypatch.setattr(runtime_kernel, "register_run_in_graph", lambda *a, **kw: None)
    monkeypatch.setattr(runtime_kernel, "save_architecture_snapshot", lambda *a, **kw: None)
    monkeypatch.setattr(runtime_kernel, "serialize_run_payload", lambda *a, **kw: {
        "payload": "ok", "run_id": "r1", "intent": "test",
        "mode": "default", "output_type": "text", "result": {}, "contract": {}
    })
    monkeypatch.setattr(runtime_kernel, "save_knowledge_object", lambda *a, **kw: None)
    monkeypatch.setattr(runtime_kernel, "graph_summary", lambda: {})
    monkeypatch.setattr(runtime_kernel, "analyze_graph", lambda **kw: {})
    monkeypatch.setattr(runtime_kernel, "get_checkpoint_file", lambda run_id: "/tmp/cp.json")

    class _DummyMemory:
        def add_record(self, r):
            pass

    monkeypatch.setattr(runtime_kernel, "SESSION_MEMORY", _DummyMemory())

    command = object.__new__(CommandObject)
    command.raw_input = "test input"
    command.intent = "test"
    command.mode = "default"

    result = runtime_kernel.run(command)

    assert not inspect.isawaitable(result), (
        "DRIFT DETECTED: runtime_kernel.run() returned an awaitable. "
        "The kernel must return a plain sync result. "
        "Do not re-introduce _SyncAsyncResult or any async wrapper inside the kernel."
    )
    assert result.summary == "ok"
    assert result.observer_status == "OK"
