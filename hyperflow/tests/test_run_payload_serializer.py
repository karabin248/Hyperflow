from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.output.run_payload import serialize_run_payload



def test_serialize_run_payload_builds_shared_top_level_envelope():
    command = build_command("🌈💎🔥🧠🔀⚡ prepare a rollout plan")
    result = run(command)

    payload = serialize_run_payload(command, result)

    assert payload["command"]["raw_input"].startswith("🌈💎🔥🧠🔀⚡")
    assert payload["intent"] == command.intent
    assert payload["mode"] == command.mode
    assert payload["output_type"] == command.output_type
    assert payload["run_id"] == result.run_id
    assert payload["contract"] == result.edde_contract
    assert payload["result"]["edde_contract"] == result.edde_contract
