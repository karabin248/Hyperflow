from hyperflow.language.command_builder import build_command


def test_build_command_planning_english_sections_by_default():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)

    assert command.intent == "planning"
    assert command.mode == "fusion"
    assert command.output_type == "plan"
    assert command.operations == ["perceive", "extract_core", "set_direction", "synthesize", "generate_options", "choose"]
    assert command.confidence in {"medium", "high"}


def test_build_command_keeps_polish_section_compatibility():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Zadanie: stwórz plan budowy Hyperflow MVP "
        "Cel: wyodrębnić kolejność modułów "
        "Format: sekcje + priorytety"
    )

    command = build_command(raw)

    assert command.intent == "planning"
    assert command.mode == "fusion"
    assert command.output_type == "plan"
    assert command.operations == ["perceive", "extract_core", "set_direction", "synthesize", "generate_options", "choose"]
    assert command.confidence == "high"
