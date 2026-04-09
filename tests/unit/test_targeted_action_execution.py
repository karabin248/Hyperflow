from hyperflow.engine.edde_orchestrator import resolve_target
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.language.command_builder import build_command


def test_runtime_state_initializes_active_target_from_target_signal() -> None:
    command = build_command("🎯 repo-alpha 💎")
    state = init_runtime_state(command)

    assert state.active_target == "repo-alpha"


def test_resolve_target_prefers_inline_target_over_active_target() -> None:
    command = build_command("🎯 repo-alpha")
    state = init_runtime_state(command)
    parsed = {"target": "repo-beta"}

    assert resolve_target(state, parsed) == "repo-beta"


def test_resolve_target_uses_runtime_state_when_inline_target_missing() -> None:
    command = build_command("🎯 repo-alpha")
    state = init_runtime_state(command)

    assert resolve_target(state, {"target": None}) == "repo-alpha"
