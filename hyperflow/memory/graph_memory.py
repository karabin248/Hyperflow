import json
from collections import Counter
from pathlib import Path
from typing import Any

from hyperflow.runtime_paths import get_graph_file


def _empty_graph() -> dict:
    return {
        "nodes": [],
        "edges": [],
    }


def load_graph(file_path: Path | None = None) -> dict:
    target = file_path or get_graph_file()

    if not target.exists():
        return _empty_graph()

    try:
        data = json.loads(target.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return _empty_graph()

    if "nodes" not in data or "edges" not in data:
        return _empty_graph()

    return data


def save_graph(graph: dict, file_path: Path | None = None) -> Path:
    target = file_path or get_graph_file()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")
    return target


def _has_node(graph: dict, node_id: str) -> bool:
    return any(node["id"] == node_id for node in graph["nodes"])


def _has_edge(graph: dict, source: str, target: str, edge_type: str) -> bool:
    return any(
        edge["source"] == source
        and edge["target"] == target
        and edge["type"] == edge_type
        for edge in graph["edges"]
    )


def add_node(
    graph: dict,
    node_id: str,
    node_type: str,
    label: str,
    metadata: dict | None = None,
) -> None:
    if _has_node(graph, node_id):
        return

    graph["nodes"].append(
        {
            "id": node_id,
            "type": node_type,
            "label": label,
            "metadata": metadata or {},
        }
    )


def add_edge(graph: dict, source: str, target: str, edge_type: str) -> None:
    if _has_edge(graph, source, target, edge_type):
        return

    graph["edges"].append(
        {
            "source": source,
            "target": target,
            "type": edge_type,
        }
    )


def _slug(text: str) -> str:
    return "_".join(text.strip().lower().split()) if text.strip() else "empty"


def register_run_in_graph(
    run_id: str,
    command: Any,
    result: Any,
    file_path: Path | None = None,
) -> dict:
    graph = load_graph(file_path)

    run_node_id = f"run:{run_id}"
    intent_node_id = f"intent:{command.intent}"
    mode_node_id = f"mode:{command.mode}"
    output_node_id = f"output:{command.output_type}"

    add_node(graph, run_node_id, "run", run_id)
    add_node(graph, intent_node_id, "intent", command.intent)
    add_node(graph, mode_node_id, "mode", command.mode)
    add_node(graph, output_node_id, "output_type", command.output_type)

    add_edge(graph, run_node_id, intent_node_id, "has_intent")
    add_edge(graph, run_node_id, mode_node_id, "has_mode")
    add_edge(graph, run_node_id, output_node_id, "has_output_type")
    add_edge(graph, intent_node_id, mode_node_id, "uses_mode")
    add_edge(graph, mode_node_id, output_node_id, "produces_output_type")

    for op in command.operations:
        op_node_id = f"operation:{op}"
        add_node(graph, op_node_id, "operation", op)
        add_edge(graph, run_node_id, op_node_id, "uses_operation")
        add_edge(graph, intent_node_id, op_node_id, "requires_operation")

    for idx, insight in enumerate(result.insights):
        insight_id = f"insight:{run_id}:{idx}:{_slug(insight)[:40]}"
        add_node(graph, insight_id, "insight", insight)
        add_edge(graph, run_node_id, insight_id, "produced_insight")
        add_edge(graph, intent_node_id, insight_id, "intent_generates_insight")

    summary_node_id = f"summary:{run_id}"
    add_node(
        graph,
        summary_node_id,
        "summary",
        result.summary,
        metadata={
            "confidence": result.confidence,
            "observer_status": result.observer_status,
        },
    )
    add_edge(graph, run_node_id, summary_node_id, "has_summary")

    save_graph(graph, file_path)
    return graph


def graph_summary(file_path: Path | None = None) -> dict:
    graph = load_graph(file_path)

    node_count = len(graph["nodes"])
    edge_count = len(graph["edges"])

    type_counter = Counter(node["type"] for node in graph["nodes"])

    intent_counter = Counter(
        node["label"] for node in graph["nodes"] if node["type"] == "intent"
    )
    mode_counter = Counter(
        node["label"] for node in graph["nodes"] if node["type"] == "mode"
    )
    operation_counter = Counter(
        node["label"] for node in graph["nodes"] if node["type"] == "operation"
    )

    recent_summaries = [
        node["label"] for node in graph["nodes"] if node["type"] == "summary"
    ][-5:]

    return {
        "node_count": node_count,
        "edge_count": edge_count,
        "node_types": dict(type_counter),
        "top_intents": intent_counter.most_common(5),
        "top_modes": mode_counter.most_common(5),
        "top_operations": operation_counter.most_common(10),
        "recent_summaries": recent_summaries[::-1],
    }