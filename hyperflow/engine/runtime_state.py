from uuid import uuid4

from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


def _resolve_initial_active_target(command: CommandObject) -> str | None:
    for route in getattr(command, "action_routes", []) or []:
        target = str(route.get("target") or "").strip()
        if route.get("emoji") == "🎯" and target:
            return None if target.lower() in {"clear", "none", "null", "-"} else target
    return None


def init_runtime_state(command: CommandObject) -> RuntimeState:
    return RuntimeState(
        run_id=str(uuid4()),
        phase="init",
        intent=command.intent,
        mode=command.mode,
        active_target=_resolve_initial_active_target(command),
    )
