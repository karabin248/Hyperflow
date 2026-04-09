from hyperflow.memory.graph_memory import load_graph


def _safe_id(node_id: str) -> str:
    return node_id.replace(":", "_").replace("-", "_").replace(".", "_").replace("/", "_").replace(" ", "_")


def _get_recent_run_ids(graph: dict, limit_runs: int = 5) -> list[str]:
    run_nodes = [n for n in graph["nodes"] if n["type"] == "run"]
    return [node["id"] for node in run_nodes[-limit_runs:]]


def _collect_subgraph(graph: dict, limit_runs: int = 5) -> tuple[list[dict], list[dict]]:
    run_ids = set(_get_recent_run_ids(graph, limit_runs=limit_runs))
    if not run_ids:
        return [], []
    selected_edges = [edge for edge in graph["edges"] if edge["source"] in run_ids]
    selected_node_ids = set(run_ids)
    for edge in selected_edges:
        selected_node_ids.add(edge["target"])
    return [node for node in graph["nodes"] if node["id"] in selected_node_ids], selected_edges


def render_graph_mermaid(limit_runs: int = 5) -> str:
    graph = load_graph()
    selected_nodes, selected_edges = _collect_subgraph(graph, limit_runs=limit_runs)
    lines = ["graph TD"]
    if not selected_nodes:
        lines.append('  empty["No graph data available"]')
        return "\n".join(lines)
    for node in selected_nodes:
        lines.append(f'  {_safe_id(node["id"])}["{str(node["label"]).replace(chr(34), chr(39))}"]')
    for edge in selected_edges:
        lines.append(f"  {_safe_id(edge["source"])} -->|{edge["type"]}| {_safe_id(edge["target"])}")
    return "\n".join(lines)


def render_graph_ascii(limit_runs: int = 5) -> str:
    graph = load_graph()
    selected_nodes, selected_edges = _collect_subgraph(graph, limit_runs=limit_runs)
    node_map = {node["id"]: node for node in selected_nodes}
    edge_map: dict[str, list[dict]] = {}
    for edge in selected_edges:
        edge_map.setdefault(edge["source"], []).append(edge)
    run_nodes = [n for n in selected_nodes if n["type"] == "run"]
    lines = ["=" * 50, "HYPERFLOW GRAPH ASCII", "=" * 50]
    if not run_nodes:
        lines.append("No graph data available.")
        return "\n".join(lines)
    for run_node in run_nodes[::-1]:
        lines.append(f"{run_node['id']}")
        outgoing = edge_map.get(run_node["id"], [])
        if not outgoing:
            lines.append("  └─ no edges"); lines.append("")
            continue
        for i, edge in enumerate(outgoing):
            connector = "└─" if i == len(outgoing) - 1 else "├─"
            target = node_map.get(edge["target"], {"label": edge["target"]})
            lines.append(f"  {connector} {edge['type']} → {target['label']}")
        lines.append("")
    return "\n".join(lines)
