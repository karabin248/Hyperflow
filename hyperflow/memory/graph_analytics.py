from collections import Counter

from hyperflow.memory.graph_memory import load_graph


def _get_recent_run_ids(graph: dict, limit_runs: int = 10) -> list[str]:
    run_nodes = [n for n in graph["nodes"] if n["type"] == "run"]
    run_nodes = run_nodes[-limit_runs:]
    return [node["id"] for node in run_nodes]


def _filter_recent_subgraph(graph: dict, limit_runs: int = 10) -> tuple[list[dict], list[dict]]:
    run_ids = set(_get_recent_run_ids(graph, limit_runs=limit_runs))
    if not run_ids:
        return [], []
    selected_edges = [edge for edge in graph["edges"] if edge["source"] in run_ids]
    selected_node_ids = set(run_ids)
    for edge in selected_edges:
        selected_node_ids.add(edge["target"])
    selected_nodes = [node for node in graph["nodes"] if node["id"] in selected_node_ids]
    return selected_nodes, selected_edges


def analyze_graph(limit_runs: int = 10) -> dict:
    graph = load_graph()
    selected_nodes, selected_edges = _filter_recent_subgraph(graph, limit_runs=limit_runs)
    node_map = {node["id"]: node for node in selected_nodes}
    intent_counter = Counter()
    mode_counter = Counter()
    operation_counter = Counter()
    output_counter = Counter()
    intent_mode_counter = Counter()
    intent_operation_counter = Counter()
    run_summaries = []
    for run_node in [n for n in selected_nodes if n["type"] == "run"]:
        run_id = run_node["id"]
        outgoing = [edge for edge in selected_edges if edge["source"] == run_id]
        run_intents, run_modes, run_operations, run_outputs, run_summary = [], [], [], [], None
        for edge in outgoing:
            target = node_map.get(edge["target"])
            if not target:
                continue
            if edge["type"] == "has_intent" and target["type"] == "intent":
                run_intents.append(target["label"]); intent_counter[target["label"]] += 1
            elif edge["type"] == "has_mode" and target["type"] == "mode":
                run_modes.append(target["label"]); mode_counter[target["label"]] += 1
            elif edge["type"] == "uses_operation" and target["type"] == "operation":
                run_operations.append(target["label"]); operation_counter[target["label"]] += 1
            elif edge["type"] == "has_output_type" and target["type"] == "output_type":
                run_outputs.append(target["label"]); output_counter[target["label"]] += 1
            elif edge["type"] == "has_summary" and target["type"] == "summary":
                run_summary = target["label"]
        for intent in run_intents:
            for mode in run_modes:
                intent_mode_counter[(intent, mode)] += 1
            for operation in run_operations:
                intent_operation_counter[(intent, operation)] += 1
        run_summaries.append({"run_id": run_id, "intents": run_intents, "modes": run_modes, "operations": run_operations, "outputs": run_outputs, "summary": run_summary})
    dominant_intent = intent_counter.most_common(1)[0][0] if intent_counter else None
    dominant_mode = mode_counter.most_common(1)[0][0] if mode_counter else None
    interpretation = []
    if dominant_intent:
        interpretation.append(f"Dominant recent intent: {dominant_intent}.")
    if dominant_mode:
        interpretation.append(f"Dominant recent mode: {dominant_mode}.")
    if intent_operation_counter:
        top_pair = intent_operation_counter.most_common(1)[0]
        interpretation.append(f"Most common intent-operation pair: {top_pair[0][0]} -> {top_pair[0][1]} ({top_pair[1]}).")
    return {
        "run_count": len([n for n in selected_nodes if n["type"] == "run"]),
        "node_count": len(selected_nodes),
        "edge_count": len(selected_edges),
        "top_intents": intent_counter.most_common(5),
        "top_modes": mode_counter.most_common(5),
        "top_operations": operation_counter.most_common(10),
        "top_output_types": output_counter.most_common(5),
        "top_intent_mode_pairs": [{"intent": k[0], "mode": k[1], "count": v} for k, v in intent_mode_counter.most_common(10)],
        "top_intent_operation_pairs": [{"intent": k[0], "operation": k[1], "count": v} for k, v in intent_operation_counter.most_common(10)],
        "recent_run_summaries": run_summaries[::-1],
        "interpretation": interpretation,
    }
