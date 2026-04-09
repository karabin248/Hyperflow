from pathlib import Path

from hyperflow.memory.graph_memory import (
    graph_summary,
    load_graph,
    register_run_in_graph,
)
from hyperflow.language.command_builder import build_command
from hyperflow.engine.runtime_kernel import run


def test_register_run_in_graph(tmp_path: Path):
    graph_file = tmp_path / "graph_memory.json"

    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    result = run(command)

    graph = register_run_in_graph("test-run-1", command, result, graph_file)

    assert "nodes" in graph
    assert "edges" in graph
    assert len(graph["nodes"]) > 0
    assert len(graph["edges"]) > 0

    loaded = load_graph(graph_file)
    assert len(loaded["nodes"]) > 0
    assert len(loaded["edges"]) > 0