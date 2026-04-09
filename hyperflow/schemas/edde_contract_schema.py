from __future__ import annotations

from typing import Any, Mapping

from hyperflow.contracts.version_policy import assert_contract_version
from hyperflow.schemas.errors import SchemaValidationError

EDDE_CONTRACT_SCHEMA: dict[str, Any] = {
    "schema": "hyperflow/edde-contract/v1",
    "type": "object",
    "required": [
        "schema",
        "contract_version",
        "trace_id",
        "status",
        "input",
        "parser",
        "timeline",
        "runtime",
        "output",
        "errors",
    ],
}

_ALLOWED_STATUS = {"ok", "fallback"}
_ALLOWED_TIMELINE_PHASES = {"DECIDE", "DO", "OUTPUT"}
_ALLOWED_NEXT_STEPS = {"DO", "OUTPUT", "DECIDE", "END"}
_ALLOWED_OUTPUT_KINDS = {
    "answer",
    "analysis",
    "blueprint",
    "json",
    "map",
    "plan",
    "report",
    "spec",
}


def _require_mapping(payload: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(payload, Mapping):
        raise SchemaValidationError(f"{label} expected object payload")
    return payload


def _require_list(payload: Any, label: str) -> list[Any]:
    if not isinstance(payload, list):
        raise SchemaValidationError(f"{label} expected array payload")
    return payload


def _require_str(payload: Any, label: str) -> str:
    if not isinstance(payload, str) or not payload.strip():
        raise SchemaValidationError(f"{label} expected non-empty string")
    return payload


def _require_bool(payload: Any, label: str) -> bool:
    if not isinstance(payload, bool):
        raise SchemaValidationError(f"{label} expected boolean payload")
    return payload


def _require_int(payload: Any, label: str) -> int:
    if not isinstance(payload, int):
        raise SchemaValidationError(f"{label} expected integer payload")
    return payload


def _validate_timeline_step(step: Any, index: int) -> None:
    data = _require_mapping(step, f"timeline[{index}]")
    phase = _require_str(data.get("phase"), f"timeline[{index}].phase")
    if phase not in _ALLOWED_TIMELINE_PHASES:
        raise SchemaValidationError(f"timeline[{index}].phase uses unsupported phase '{phase}'")

    _require_str(data.get("trace_id"), f"timeline[{index}].trace_id")
    _require_mapping(data.get("input"), f"timeline[{index}].input")
    _require_list(data.get("plan"), f"timeline[{index}].plan")
    _require_mapping(data.get("results"), f"timeline[{index}].results")
    _require_mapping(data.get("assessment"), f"timeline[{index}].assessment")

    constraints = _require_mapping(data.get("constraints"), f"timeline[{index}].constraints")
    for key in ("safe", "sandboxed", "llm_no_direct_ffi"):
        _require_bool(constraints.get(key), f"timeline[{index}].constraints.{key}")

    next_step = _require_str(data.get("next_step"), f"timeline[{index}].next_step")
    if next_step not in _ALLOWED_NEXT_STEPS:
        raise SchemaValidationError(
            f"timeline[{index}].next_step uses unsupported transition '{next_step}'"
        )


def validate_edde_contract(payload: Any) -> None:
    data = _require_mapping(payload, "edde_contract")

    for key in EDDE_CONTRACT_SCHEMA["required"]:
        if key not in data:
            raise SchemaValidationError(f"edde_contract missing required field '{key}'")

    schema_name = _require_str(data.get("schema"), "edde_contract.schema")
    if schema_name != EDDE_CONTRACT_SCHEMA["schema"]:
        raise SchemaValidationError(f"edde_contract schema mismatch '{schema_name}'")

    contract_version = _require_str(data.get("contract_version"), "edde_contract.contract_version")
    try:
        assert_contract_version(contract_version)
    except ValueError as exc:
        raise SchemaValidationError(str(exc)) from exc

    _require_str(data.get("trace_id"), "edde_contract.trace_id")

    status = _require_str(data.get("status"), "edde_contract.status")
    if status not in _ALLOWED_STATUS:
        raise SchemaValidationError(f"edde_contract.status uses unsupported value '{status}'")

    input_block = _require_mapping(data.get("input"), "edde_contract.input")
    _require_str(input_block.get("raw_prompt"), "edde_contract.input.raw_prompt")
    if not isinstance(input_block.get("emoji_run"), str):
        raise SchemaValidationError("edde_contract.input.emoji_run expected string payload")
    if not isinstance(input_block.get("core_text"), str):
        raise SchemaValidationError("edde_contract.input.core_text expected string payload")

    parser = _require_mapping(data.get("parser"), "edde_contract.parser")
    _require_list(parser.get("tokens"), "edde_contract.parser.tokens")
    _require_list(parser.get("matched_sequences"), "edde_contract.parser.matched_sequences")
    _require_list(parser.get("resolved_edde_phase"), "edde_contract.parser.resolved_edde_phase")
    _require_list(parser.get("resolved_output_types"), "edde_contract.parser.resolved_output_types")
    _require_list(parser.get("runtime_output_types"), "edde_contract.parser.runtime_output_types")
    _require_list(parser.get("trace"), "edde_contract.parser.trace")
    _require_list(parser.get("parser_decisions"), "edde_contract.parser.parser_decisions")
    _require_str(parser.get("resolution_policy"), "edde_contract.parser.resolution_policy")

    timeline = _require_list(data.get("timeline"), "edde_contract.timeline")
    if len(timeline) != 3:
        raise SchemaValidationError("edde_contract.timeline must contain exactly 3 EDDE phases")
    for index, step in enumerate(timeline):
        _validate_timeline_step(step, index)

    runtime = _require_mapping(data.get("runtime"), "edde_contract.runtime")
    _require_list(runtime.get("flow"), "edde_contract.runtime.flow")
    _require_list(runtime.get("pipeline_path"), "edde_contract.runtime.pipeline_path")
    _require_mapping(
        runtime.get("pipeline_stage_map"),
        "edde_contract.runtime.pipeline_stage_map",
    )
    observer = _require_mapping(runtime.get("observer"), "edde_contract.runtime.observer")
    _require_str(observer.get("status"), "edde_contract.runtime.observer.status")
    mps = _require_mapping(runtime.get("mps"), "edde_contract.runtime.mps")
    _require_int(mps.get("level"), "edde_contract.runtime.mps.level")
    _require_str(mps.get("risk_level"), "edde_contract.runtime.mps.risk_level")
    _require_mapping(mps.get("profile"), "edde_contract.runtime.mps.profile")
    graph = _require_mapping(runtime.get("graph"), "edde_contract.runtime.graph")
    _require_mapping(graph.get("summary"), "edde_contract.runtime.graph.summary")
    _require_mapping(graph.get("analytics"), "edde_contract.runtime.graph.analytics")

    output = _require_mapping(data.get("output"), "edde_contract.output")
    kind = _require_str(output.get("kind"), "edde_contract.output.kind")
    if kind not in _ALLOWED_OUTPUT_KINDS:
        raise SchemaValidationError(f"edde_contract.output.kind uses unsupported value '{kind}'")
    _require_mapping(output.get("payload"), "edde_contract.output.payload")

    errors = _require_list(data.get("errors"), "edde_contract.errors")
    if not all(isinstance(item, str) for item in errors):
        raise SchemaValidationError("edde_contract.errors expected list[str]")
