import asyncio
from hyperflow.language.command_builder import build_command
from hyperflow.runtime_kernel import run
from hyperflow.memory.graph_memory import graph_summary


def test_graph_summary_returns_counts(tmp_path, monkeypatch) -> None:
    monkeypatch.setenv("HYPERFLOW_STORAGE_DIR", str(tmp_path / "storage"))
    cmd = build_command("🧠🔥 graph summary test")
    result = asyncio.run(run(cmd))
    assert result.insights is not None
    summary = graph_summary()
    assert "node_count" in summary
    assert "edge_count" in summary
