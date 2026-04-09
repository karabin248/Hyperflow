from hyperflow.engine.runtime_kernel import run
import hyperflow.engine.runtime_kernel as runtime_kernel
import hyperflow.schemas.edde_contract_schema as contract_schema
from hyperflow.schemas.errors import SchemaValidationError
from hyperflow.language.command_builder import build_command
from hyperflow.schemas.edde_contract_schema import validate_edde_contract


def test_runtime_attaches_valid_edde_contract():
    command = build_command("🌈💎🔥🧠🔀⚡ Write a definition of entropy in simple words")
    result = run(command)

    assert getattr(result, "run_id", "")
    contract = getattr(result, "edde_contract", None)
    assert isinstance(contract, dict)
    validate_edde_contract(contract)
    assert contract["trace_id"] == result.run_id
    assert [step["phase"] for step in contract["timeline"]] == [
        "DECIDE",
        "DO",
        "OUTPUT",
    ]


def test_contract_validator_rejects_missing_required_field():
    payload = {
        "schema": "hyperflow/edde-contract/v1",
        "contract_version": "1.0.0",
        "trace_id": "x",
        "status": "ok",
        "input": {"raw_prompt": "x", "emoji_run": "", "core_text": "x"},
        "parser": {"tokens": [], "matched_sequences": [], "resolved_edde_phase": [], "resolved_output_types": [], "runtime_output_types": [], "trace": [], "parser_decisions": [], "resolution_policy": "longest_match_first"},
        "timeline": [],
        "runtime": {"pipeline_path": [], "pipeline_stage_map": {}},
        "output": {"kind": "answer", "payload": {}},
    }
    try:
        validate_edde_contract(payload)
    except SchemaValidationError as exc:
        assert "missing required field 'errors'" in str(exc)
    else:  # pragma: no cover
        raise AssertionError("expected SchemaValidationError")


def test_runtime_contract_includes_mps_and_graph_context():
    command = build_command("🌈💎🔥🧠🔀⚡ Create a list of 3 examples of AI use in medicine")
    result = run(command)
    contract = getattr(result, "edde_contract", None)

    assert contract
    runtime = contract["runtime"]
    assert runtime["mps"]["level"] >= 1
    assert runtime["mps"]["profile"]["name"]
    assert "node_count" in runtime["graph"]["summary"] or runtime["graph"]["summary"] == {}
    assert "run_count" in runtime["graph"]["analytics"] or runtime["graph"]["analytics"] == {}

def test_schema_module_only_validates_and_runtime_uses_output_builder():
    assert not hasattr(contract_schema, "build_edde_contract")
    assert runtime_kernel.build_edde_contract.__module__ == "hyperflow.output.edde_contract"



def test_runtime_contract_safe_constraint_tracks_safe_mode_flag():
    default_result = run(build_command("🌈💎🔥🧠🔀⚡ Prepare a rollout plan"))
    safe_result = run(build_command("🛡️ 🌈💎🔥🧠🔀⚡ Prepare a rollout plan"))

    default_flags = [step["constraints"]["safe"] for step in default_result.edde_contract["timeline"]]
    safe_flags = [step["constraints"]["safe"] for step in safe_result.edde_contract["timeline"]]

    assert default_flags == [False, False, False]
    assert safe_flags == [True, True, True]
