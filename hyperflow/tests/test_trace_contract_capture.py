from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.memory.traces import load_recent_traces


def test_trace_record_captures_v1_contract_phase_and_next_step():
    command = build_command("🌈💎🔥🧠🔀⚡ Write a definition of entropy in simple words")
    result = run(command)
    traces = load_recent_traces(limit=1)

    assert traces
    trace = traces[0]
    assert trace["run_id"] == result.run_id
    assert trace["edde_phase"] == "OUTPUT"
    assert trace["edde_next_step"] in {"DECIDE", "END"}
