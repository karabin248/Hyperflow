from hyperflow.engine.planner import build_plan
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.language.command_builder import build_command


def test_planner_uses_english_sections_by_default():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    state = init_runtime_state(command)
    plan = build_plan(command, state)

    assert "align with goal" in plan
    assert "adapt to requested format" in plan


def test_planner_keeps_polish_section_compatibility():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Zadanie: stwórz plan budowy Hyperflow MVP "
        "Cel: wyodrębnić kolejność modułów "
        "Format: sekcje + priorytety"
    )

    command = build_command(raw)
    state = init_runtime_state(command)
    plan = build_plan(command, state)

    assert "align with goal" in plan
    assert "adapt to requested format" in plan
