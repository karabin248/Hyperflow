from pathlib import Path

from hyperflow.memory.graph_memory import graph_summary, register_run_in_graph
from hyperflow.language.command_builder import build_command
from hyperflow.engine.runtime_kernel import run


def test_graph_summary_returns_counts(tmp_path: Path):
    graph_file = tmp_path / "graph_memory.json"

    raw = (
        "🧠💎 "
        "Task: make a short analysis of the Hyperflow core "
        "Goal: extract the most important modules "
        "Format: list"
    )

    command = build_command(raw)
    result = run(command)

    register_run_in_graph("test-run-2", command, result, graph_file)

    summary = graph_summary(graph_file)

    assert summary["node_count"] > 0
    assert summary["edge_count"] > 0
    assert "top_intents" in summary
    assert "top_operations" in summary