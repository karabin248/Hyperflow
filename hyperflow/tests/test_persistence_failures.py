from __future__ import annotations

from hyperflow.engine import runtime_kernel
from hyperflow.language.command_builder import build_command


def _raise_oserror(*_args, **_kwargs):
    raise OSError("disk unavailable")


def test_run_degrades_when_persistence_writes_fail(monkeypatch) -> None:
    raw = "🌈💎🔥🧠🔀⚡ Task: prepare an MVP rollout plan"
    command = build_command(raw)

    monkeypatch.setattr(runtime_kernel, "append_trace", _raise_oserror)
    monkeypatch.setattr(runtime_kernel, "save_knowledge_object", _raise_oserror)
    monkeypatch.setattr(runtime_kernel, "register_run_in_graph", _raise_oserror)

    result = runtime_kernel.run(command)

    assert result.run_id
    assert result.edde_contract["schema"] == "hyperflow/edde-contract/v1"
    assert result.summary
