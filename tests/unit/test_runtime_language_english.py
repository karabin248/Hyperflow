from hyperflow.engine.synthesis import build_summary
from hyperflow.language.command_builder import build_command
from hyperflow.memory.graph_reasoning import reason_over_graph
from hyperflow.memory.self_profile import build_self_profile
from hyperflow.engine.runtime_kernel import run


def test_direct_entropy_artifact_is_english_for_write_prompt():
    command = build_command("🌈💎🔥🧠🔀⚡ Write a definition of entropy in simple words")
    summary = build_summary(command, {})

    assert summary.startswith("Entropy is a measure")
    assert "miara" not in summary


def test_direct_entropy_artifact_is_english_for_define_prompt():
    command = build_command("🌈💎🔥🧠🔀⚡ Define entropy in simple words")
    summary = build_summary(command, {})

    assert summary.startswith("Entropy is a measure")


def test_self_profile_and_graph_reasoning_are_english():
    planning = build_command(
        "🌈💎🔥🧠🔀⚡ Task: create a Hyperflow MVP build plan Goal: extract module order Format: sections + priorities"
    )
    analysis = build_command(
        "🧠💎 Task: make a short analysis of the Hyperflow core Goal: extract the most important modules Format: list"
    )

    run(planning)
    run(planning)
    run(analysis)

    profile = build_self_profile(limit_runs=5)
    reasoning = reason_over_graph(limit_runs=5)

    assert profile["short_self_description"].startswith("Hyperflow currently operates")
    assert "Dominująca" not in profile["narrative_summary"]
    assert any(item.startswith("The ") for item in reasoning["findings"])
    assert all("System" not in item for item in reasoning["findings"])


def test_english_prompt_heuristics_are_first_class():
    from hyperflow.language.command_builder import build_command

    command = build_command("Task: explain the architecture and provide instructions in a short format")
    assert command.intent == "documentation"
    assert command.output_type == "spec"
    assert "document" in command.operations
    assert "concise_output" in command.constraints


def test_english_mapping_and_cleanup_heuristics_are_supported():
    from hyperflow.language.command_builder import build_command

    map_command = build_command("Task: map connections across layers and show an ascii map")
    assert map_command.intent == "mapping"
    assert map_command.output_type == "map"
    assert "map_relations" in map_command.operations

    cleanup_command = build_command("Please clean up the repo and remove stale files")
    assert cleanup_command.intent == "cleanup"


def test_english_blueprint_and_deep_output_constraints_are_supported():
    from hyperflow.language.command_builder import build_command

    command = build_command("Build a function in full code form")
    assert command.intent == "build"
    assert command.output_type == "blueprint"
    assert command.output_subtype == "code_structure"
    assert "build_structure" in command.operations
    assert "deep_output" in command.constraints
