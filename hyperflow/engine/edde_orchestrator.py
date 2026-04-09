from __future__ import annotations

from hyperflow.config import get_pipeline_stage_aliases
from hyperflow.engine.reasoning import (
    run_discover_phase,
    run_do_phase,
    run_extract_phase,
)
from hyperflow.engine.synthesis import run_evaluate_phase
from hyperflow.engine.action_registry import run_action, run_action_on_node
from hyperflow.language.action_router import is_valid_target
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


def _annotate_bundle(bundle: dict, runtime_phase: str) -> dict:
    enriched = dict(bundle)
    enriched["runtime_phase"] = runtime_phase
    enriched["pipeline_aliases"] = get_pipeline_stage_aliases().get(runtime_phase, [runtime_phase])
    return enriched


def resolve_target(state: RuntimeState, parsed: dict) -> str | None:
    inline_target = str(parsed.get("target") or "").strip()
    if inline_target:
        return inline_target
    active_target = str(getattr(state, "active_target", "") or "").strip()
    return active_target or None


def _maybe_update_active_target(state: RuntimeState, parsed: dict) -> bool:
    if parsed.get("emoji") != "🎯":
        return False

    target = str(parsed.get("target") or parsed.get("arguments", {}).get("target") or "").strip()
    if not target:
        return False

    if target.lower() in {"clear", "none", "null", "-"}:
        state.active_target = None
    elif is_valid_target(target):
        state.active_target = target
    else:
        return False
    return True


def _execute_action_routes(command: CommandObject, state: RuntimeState) -> list[dict]:
    executions: list[dict] = []

    for parsed in command.parser_trace.get("action_routes", []):
        if _maybe_update_active_target(state, parsed):
            executions.append(
                {
                    "signal": parsed.get("signal") or parsed.get("emoji"),
                    "action_id": parsed.get("action_id"),
                    "target": state.active_target,
                    "status": "target_set" if state.active_target else "target_cleared",
                }
            )
            continue

        signal = str(parsed.get("action_id") or parsed.get("signal") or parsed.get("emoji") or "").strip()
        if not signal:
            continue

        target = resolve_target(state, parsed)
        payload = {
            "arguments": dict(parsed.get("arguments", {})),
            "runtime_state": state,
            "command": command,
            "parsed": parsed,
        }
        result = run_action_on_node(signal, target, **payload) if target else run_action(signal, **payload)
        executions.append(
            {
                "signal": parsed.get("signal") or parsed.get("emoji"),
                "action_id": parsed.get("action_id"),
                "target": target,
                "scope": "node" if target else "global",
                "executed": result is not None,
            }
        )

    return executions


def run_edde(command: CommandObject, state: RuntimeState) -> dict:
    action_execution = _execute_action_routes(command, state)

    extract_bundle = _annotate_bundle(run_extract_phase(command, state), "extract")
    decision_bundle = _annotate_bundle(
        run_discover_phase(command, state, extract_bundle),
        "discover",
    )
    draft_result = _annotate_bundle(run_do_phase(command, state, decision_bundle), "do")
    final_bundle = _annotate_bundle(run_evaluate_phase(command, state, draft_result), "evaluate")

    final_bundle["pipeline_path"] = [
        alias
        for phase in ("extract", "discover", "do", "evaluate")
        for alias in get_pipeline_stage_aliases().get(phase, [phase])
    ]
    final_bundle["pipeline_stage_map"] = get_pipeline_stage_aliases()
    final_bundle["resolved_edde_phase_hints"] = command.parser_trace.get("resolved_edde_phase", [])
    final_bundle["resolved_output_hints"] = command.parser_trace.get("resolved_output_types", [])
    final_bundle["emoji_control"] = {
        "matched_combo": command.parser_trace.get("matched_combo"),
        "matched_preset": command.parser_trace.get("matched_preset"),
        "primary_status": command.parser_trace.get("primary_status"),
    }
    final_bundle["action_execution"] = action_execution
    final_bundle["active_target"] = state.active_target
    final_bundle["llm_source"] = draft_result.get("source", "stub")
    final_bundle["llm_model"] = draft_result.get("model")

    state.partial_results.extend([extract_bundle, decision_bundle, draft_result])
    state.insights.extend(final_bundle.get("final_insights", []))
    state.next_step = final_bundle.get("next_step", "")

    return final_bundle
