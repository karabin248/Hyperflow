from __future__ import annotations

from hyperflow.config import get_mps_regulator_config
from hyperflow.control.mps_profiles import MPS_PROFILES
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


def _needs_core_attention(command: CommandObject) -> bool:
    token_set = set(command.tokens)
    operations = set(command.operations)
    return (
        command.intent in {"planning", "build"}
        and (
            "💎" in token_set
            or "extract_core" in operations
            or command.output_type in {"plan", "blueprint"}
        )
    )


def resolve_mps_level(command: CommandObject) -> int:
    if command.mode == "safe":
        return 1
    if command.mode == "fusion":
        return 6
    if _needs_core_attention(command):
        return 5
    if command.mode == "final" or command.intensity == "boosted":
        return 4
    if command.mode in {"analysis", "build"}:
        return 3
    return 2


def apply_mps_profile(state: RuntimeState) -> RuntimeState:
    profile = MPS_PROFILES.get(state.mps_level, MPS_PROFILES[2])
    state.mps_state = str(profile.get("name", "Stabilize"))
    state.risk_state = str(profile.get("risk_state", "medium" if state.mps_level >= 4 else "low"))
    state.risk_level = state.risk_state
    state.observer_rigor = str(profile.get("observer_rigor", "medium"))
    state.next_step = f"profile:{state.mps_state}"
    return state


def reduce_mps(state: RuntimeState) -> RuntimeState:
    safe_reroute = get_mps_regulator_config().get("safe_reroute", {})
    strategy = str(safe_reroute.get("strategy", "return_to_core"))

    if strategy == "return_to_core":
        state.mps_level = 2
    else:
        state.mps_level = max(1, state.mps_level - 1)

    profile = MPS_PROFILES.get(state.mps_level, MPS_PROFILES[2])
    state.mps_state = str(profile.get("name", "Stabilize"))
    state.risk_state = str(profile.get("risk_state", "low"))
    state.risk_level = state.risk_state
    state.observer_rigor = str(profile.get("observer_rigor", "high"))
    state.next_step = f"profile:{state.mps_state}"
    return state
