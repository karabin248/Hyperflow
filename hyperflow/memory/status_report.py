from datetime import datetime, timezone

from hyperflow.memory.graph_analytics import analyze_graph
from hyperflow.memory.graph_memory import graph_summary
from hyperflow.memory.graph_reasoning import reason_over_graph
from hyperflow.memory.self_profile import build_self_profile
from hyperflow.memory.traces import load_recent_traces
from hyperflow.version import get_version


def _assess_system_health(
    run_count: int,
    stable_core_operations: list[str],
    dominant_work_style: str,
) -> str:
    if run_count >= 8 and len(stable_core_operations) >= 3 and dominant_work_style != "mixed":
        return "stable-operational"
    if run_count >= 4 and len(stable_core_operations) >= 2:
        return "stabilizing"
    return "early-active"


def _build_recommendations(
    health: str,
    dominant_intent: str | None,
    satellite_modes: list[str],
) -> list[str]:
    recommendations = []

    if health == "early-active":
        recommendations.append("Run more commands to stabilize behavior patterns.")
        recommendations.append("Strengthen repeatable operational core before adding new layers.")
    elif health == "stabilizing":
        recommendations.append("Preserve stable core and expand output/reporting layers.")
    else:
        recommendations.append("System is stable enough for higher-order orchestration and reporting.")

    if dominant_intent == "planning":
        recommendations.append("Add stronger execution/report layers to complement planning dominance.")
    elif dominant_intent == "analysis":
        recommendations.append("Add synthesis/build layers to complement analysis dominance.")

    if satellite_modes:
        recommendations.append(
            f"Monitor satellite behaviors for growth or consolidation: {', '.join(satellite_modes)}."
        )

    return recommendations


def build_status_report(limit_runs: int = 10) -> dict:
    traces = load_recent_traces(limit=limit_runs)
    summary = graph_summary()
    analytics = analyze_graph(limit_runs=limit_runs)
    reasoning = reason_over_graph(limit_runs=limit_runs)
    profile = build_self_profile(limit_runs=limit_runs)

    run_count = analytics["run_count"]
    dominant_work_style = profile["dominant_work_style"]
    dominant_intent = reasoning["dominant_intent"]
    dominant_mode = reasoning["dominant_mode"]
    stable_core_operations = profile["core_operating_kernel"]
    satellite_modes = profile["satellite_modes"]

    health = _assess_system_health(
        run_count=run_count,
        stable_core_operations=stable_core_operations,
        dominant_work_style=dominant_work_style,
    )

    recent_summaries = [item.get("summary", "") for item in traces[:5]]

    report = {
        "report_timestamp": datetime.now(timezone.utc).isoformat(),
        "system_name": "Hyperflow",
        "version": get_version(),
        "status": health,
        "development_phase": profile["development_phase"],
        "dominant_work_style": dominant_work_style,
        "dominant_intent": dominant_intent,
        "dominant_mode": dominant_mode,
        "core_operating_kernel": stable_core_operations,
        "satellite_modes": satellite_modes,
        "graph_snapshot": {
            "nodes": summary["node_count"],
            "edges": summary["edge_count"],
            "top_intents": summary["top_intents"],
            "top_modes": summary["top_modes"],
            "top_operations": summary["top_operations"],
        },
        "recent_activity": {
            "run_count": run_count,
            "recent_summaries": recent_summaries,
        },
        "reasoning_findings": reasoning["findings"],
        "short_self_description": profile["short_self_description"],
        "narrative_summary": profile["narrative_summary"],
        "recommendations": _build_recommendations(
            health=health,
            dominant_intent=dominant_intent,
            satellite_modes=satellite_modes,
        ),
    }

    return report
