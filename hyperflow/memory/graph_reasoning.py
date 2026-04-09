from hyperflow.memory.graph_analytics import analyze_graph


def _safe_ratio(part: int, whole: int) -> float:
    if whole <= 0:
        return 0.0
    return part / whole


def reason_over_graph(limit_runs: int = 10) -> dict:
    analytics = analyze_graph(limit_runs=limit_runs)
    run_count = analytics["run_count"]
    top_intents = analytics["top_intents"]
    top_modes = analytics["top_modes"]
    top_operations = analytics["top_operations"]
    top_intent_mode_pairs = analytics["top_intent_mode_pairs"]
    top_intent_operation_pairs = analytics["top_intent_operation_pairs"]
    findings = []
    profile = "mixed"
    dominant_intent = None
    dominant_mode = None
    secondary_intent = None
    satellite_intents = []
    stable_core_operations = []
    if top_intents:
        dominant_intent, dominant_intent_count = top_intents[0]
        dominant_ratio = _safe_ratio(dominant_intent_count, run_count)
        if dominant_ratio >= 0.7:
            findings.append(f"The system has recently operated mainly in '{dominant_intent}' intent.")
            profile = f"{dominant_intent}-dominant"
        elif dominant_ratio >= 0.5:
            findings.append(f"The system leans strongly toward '{dominant_intent}', but it is not completely uniform.")
            profile = f"{dominant_intent}-leaning"
        else:
            findings.append("The system shows a more mixed activity profile without one absolutely dominant intent.")
        if len(top_intents) > 1:
            secondary_intent, secondary_count = top_intents[1]
            if secondary_count > 0:
                findings.append(f"'{secondary_intent}' appears as a secondary supporting pattern.")
        for label, count in top_intents[1:]:
            if count <= 1:
                satellite_intents.append(label)
        if satellite_intents:
            findings.append(f"Less frequent intents behave like satellites: {', '.join(satellite_intents)}.")
    if top_modes:
        dominant_mode, dominant_mode_count = top_modes[0]
        dominant_mode_ratio = _safe_ratio(dominant_mode_count, run_count)
        if dominant_mode_ratio >= 0.7:
            findings.append(f"The dominant recent mode is '{dominant_mode}'.")
        else:
            findings.append(f"Mode '{dominant_mode}' is the most common, but other execution paths are visible too.")
    if top_operations:
        stable_core_operations = [label for label, count in top_operations if count >= max(2, run_count // 2)]
        if stable_core_operations:
            findings.append(f"The Hyperflow operating core is stable: {', '.join(stable_core_operations)}.")
    if top_intent_mode_pairs:
        pair = top_intent_mode_pairs[0]
        findings.append(f"The strongest relational pattern is {pair['intent']} -> {pair['mode']}.")
    if top_intent_operation_pairs:
        top_pair = top_intent_operation_pairs[0]
        findings.append(f"The most frequent intent-operation pair is {top_pair['intent']} -> {top_pair['operation']}.")
    high_level_summary_parts = []
    if dominant_intent:
        high_level_summary_parts.append(f"dominant intent: {dominant_intent}")
    if dominant_mode:
        high_level_summary_parts.append(f"dominant mode: {dominant_mode}")
    if stable_core_operations:
        high_level_summary_parts.append(f"stable core: {', '.join(stable_core_operations)}")
    high_level_summary = "; ".join(high_level_summary_parts) if high_level_summary_parts else "no strong graph reasoning available"
    return {
        "profile": profile,
        "dominant_intent": dominant_intent,
        "dominant_mode": dominant_mode,
        "secondary_intent": secondary_intent,
        "satellite_intents": satellite_intents,
        "stable_core_operations": stable_core_operations,
        "findings": findings,
        "high_level_summary": high_level_summary,
        "analytics": analytics,
    }
