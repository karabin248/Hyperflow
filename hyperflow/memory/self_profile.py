from hyperflow.memory.graph_reasoning import reason_over_graph


def build_self_profile(limit_runs: int = 10) -> dict:
    reasoning = reason_over_graph(limit_runs=limit_runs)
    analytics = reasoning["analytics"]
    dominant_intent = reasoning["dominant_intent"]
    dominant_mode = reasoning["dominant_mode"]
    secondary_intent = reasoning["secondary_intent"]
    stable_core_operations = reasoning["stable_core_operations"]
    satellite_intents = reasoning["satellite_intents"]
    work_style = "mixed"
    if dominant_intent and dominant_mode:
        work_style = f"{dominant_intent}-{dominant_mode}"
    elif dominant_intent:
        work_style = dominant_intent
    run_count = analytics["run_count"]
    development_phase = "early-forming"
    if run_count >= 5 and stable_core_operations:
        development_phase = "stabilizing"
    if run_count >= 8 and len(stable_core_operations) >= 2:
        development_phase = "structured-operational"
    if run_count >= 12 and dominant_intent and dominant_mode:
        development_phase = "self-consistent"
    if dominant_intent == "planning" and dominant_mode == "fusion":
        short_description = "Hyperflow currently operates as a planning-and-integration system, with emphasis on ordering, synthesis, option comparison, and choice."
    elif dominant_intent == "analysis":
        short_description = "Hyperflow currently operates as an analytical system, focused on extracting the core signal and interpreting it."
    else:
        short_description = "Hyperflow currently operates with a mixed profile, combining analysis, structure, and iterative construction."
    satellite_summary = ", ".join(satellite_intents) if satellite_intents else "none"
    narrative_summary = (
        f"Hyperflow has a '{work_style}' profile. "
        f"The dominant intent is '{dominant_intent}', and the dominant mode is '{dominant_mode}'. "
        f"Operating core: {', '.join(stable_core_operations) if stable_core_operations else 'none'}. "
        f"Satellite modes: {satellite_summary}. "
        f"Current development phase: {development_phase}."
    )
    return {
        "dominant_work_style": work_style,
        "core_operating_kernel": stable_core_operations,
        "satellite_modes": satellite_intents,
        "development_phase": development_phase,
        "short_self_description": short_description,
        "technical_summary": {"work_style": work_style, "dominant_intent": dominant_intent, "dominant_mode": dominant_mode, "secondary_intent": secondary_intent, "stable_core_operations": stable_core_operations, "satellite_intents": satellite_intents, "development_phase": development_phase},
        "narrative_summary": narrative_summary,
        "reasoning_findings": reasoning["findings"],
    }
