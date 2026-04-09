from hyperflow.language.command_builder import build_command
from hyperflow.output.base import BaseOutput
from hyperflow.output.output_pipeline import format_output
from hyperflow.schemas.observer_schema import ObserverReport
from hyperflow.schemas.output_schema import BaseOutput as SchemaBaseOutput, OutputObject
from hyperflow.engine.runtime_state import init_runtime_state


def test_output_schema_alias_points_to_canonical_base_output():
    assert SchemaBaseOutput is BaseOutput
    assert OutputObject is BaseOutput


def test_format_output_returns_canonical_output_object_with_run_id():
    command = build_command("🌈💎🔥🧠🔀⚡ create a rollout plan")
    state = init_runtime_state(command)
    state.plan = ["step 1", "step 2"]
    final_bundle = {
        "summary": "Rollout summary",
        "final_insights": ["Insight A"],
        "actions": ["Action A"],
        "next_step": "DECIDE",
        "confidence": "medium-high",
    }
    observer = ObserverReport(observer_status="OK", confidence_adjustment="none")

    result = format_output(command, state, final_bundle, observer)

    assert isinstance(result, BaseOutput)
    assert result.run_id == state.run_id
    assert result.kind == command.output_type
    assert result.plan == state.plan
    assert result.edde_contract == {}


def test_output_pipeline_annotations_use_canonical_base_output():
    assert format_output.__annotations__["return"] is BaseOutput
