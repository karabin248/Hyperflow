from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command


def test_runtime_kernel_end_to_end():
    raw = (
        "🌈💎🔥🧠🔀⚡ "
        "Task: create a Hyperflow MVP build plan "
        "Goal: extract module order "
        "Format: sections + priorities"
    )

    command = build_command(raw)
    result = run(command)

    assert result.intent == "planning"
    assert result.mode == "fusion"
    assert command.operations == ["perceive", "extract_core", "set_direction", "synthesize", "generate_options", "choose"]
    assert isinstance(result.plan, list)
    assert len(result.plan) > 0
    assert isinstance(result.summary, str)
    assert len(result.summary) > 0
    assert isinstance(result.insights, list)

def test_runtime_result_uses_validated_v1_contract_only():
    command = build_command("🌈💎🔥🧠🔀⚡ create a rollout plan")
    result = run(command)

    assert result.edde_contract["schema"] == "hyperflow/edde-contract/v1"
    assert len(result.edde_contract["timeline"]) == 3
    assert result.edde_contract["output"]["payload"]["run_id"] == result.run_id

def test_runtime_preserves_canonical_full_combo_phase_order():
    command = build_command("🌈💎🔥🧠🔀⚡ prepare a rollout plan")
    result = run(command)

    expected = ["scan", "extract", "build", "reason", "remix", "deliver"]
    assert command.parser_trace["resolved_edde_phase"] == expected
    assert result.edde_contract["parser"]["resolved_edde_phase"] == expected

