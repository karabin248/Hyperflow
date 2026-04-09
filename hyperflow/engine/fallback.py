from __future__ import annotations

from hyperflow.config import get_mps_regulator_config
from hyperflow.control.mps_controller import reduce_mps
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


def apply_fallback(
    command: CommandObject,
    state: RuntimeState,
    final_bundle: dict,
) -> tuple[RuntimeState, dict]:
    safe_reroute = get_mps_regulator_config().get("safe_reroute", {})
    strategy = str(safe_reroute.get("strategy", "return_to_core"))
    reroute_steps = list(safe_reroute.get("steps", []))

    state = reduce_mps(state)

    simplified = {
        "summary": (
            f"Fallback activated for intent '{command.intent}'. "
            f"Applying '{strategy}' recovery path and returning simplified structured output."
        ),
        "final_insights": final_bundle.get("final_insights", [])[:2],
        "actions": final_bundle.get("actions", [])[:2],
        "confidence": "low-medium",
        "next_step": strategy,
        "reroute_steps": reroute_steps,
    }

    if command.output_type == "plan" and not state.plan:
        state.plan = reroute_steps or ["clarify task", "reduce scope", "retry execution"]

    return state, simplified
