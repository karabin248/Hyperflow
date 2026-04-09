from hyperflow.language.command_builder import build_command
from hyperflow.engine.runtime_kernel import run
from hyperflow.memory.graph_visualizer import render_graph_ascii, render_graph_mermaid


def test_graph_renderers_return_text():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    run(command)

    mermaid = render_graph_mermaid(limit_runs=2)
    ascii_view = render_graph_ascii(limit_runs=2)

    assert "graph TD" in mermaid
    assert "HYPERFLOW GRAPH ASCII" in ascii_view