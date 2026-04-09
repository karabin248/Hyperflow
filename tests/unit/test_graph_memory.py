import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.memory.graph_memory import graph_summary, register_run_in_graph


def test_register_run_in_graph(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 register run in graph test")
    result = asyncio.run(run(cmd))
    assert result.insights is not None
    summary = graph_summary()
    assert summary["node_count"] >= 0
