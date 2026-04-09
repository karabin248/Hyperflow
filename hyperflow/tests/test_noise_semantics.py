from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.memory.traces import build_trace_record


def test_trace_record_captures_output_subtype_and_resolved_subtypes():
    command = build_command("👁️🔍🧠🧱⚙️")
    result = run(command)
    trace = build_trace_record("run-1", command, result)

    assert trace["output_subtype"] == "visual_analysis"
    assert "visual_analysis" in trace["resolved_output_subtypes"]
    assert result.to_dict()["output_subtype"] == "visual_analysis"
