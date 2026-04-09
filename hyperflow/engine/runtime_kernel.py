from hyperflow.control.mps_controller import apply_mps_profile, resolve_mps_level
from hyperflow.control.observer import build_observer_contract, final_check, pre_run_check
from hyperflow.engine.edde_orchestrator import run_edde
from hyperflow.engine.fallback import apply_fallback
from hyperflow.engine.planner import build_plan
from hyperflow.engine.runtime_state import init_runtime_state
from hyperflow.memory.graph_analytics import analyze_graph
from hyperflow.memory.graph_memory import graph_summary, register_run_in_graph
from hyperflow.memory.knowledge_store import save_knowledge_object
from hyperflow.memory.session_memory import SESSION_MEMORY, SessionRecord
from hyperflow.memory.traces import append_trace, build_trace_record
from hyperflow.checkpoint.snapshot import save_architecture_snapshot
from hyperflow.output.edde_contract import build_edde_contract
from hyperflow.runtime_paths import get_checkpoint_file
from hyperflow.output.output_pipeline import format_output
from hyperflow.output.run_payload import serialize_run_payload
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.edde_contract_schema import validate_edde_contract


def _best_effort_persist(operation, *args, **kwargs) -> None:
    try:
        operation(*args, **kwargs)
    except OSError:
        return


def run(command: CommandObject):
    if not isinstance(command, CommandObject):
        raise ValueError(
            "runtime_kernel.run only accepts CommandObject/EDDE execution path, got "
            f"{type(command).__name__!r}."
        )

    state = init_runtime_state(command)

    pre_report = pre_run_check(command)
    state.observer_status = pre_report.observer_status

    state.mps_level = resolve_mps_level(command)
    state = apply_mps_profile(state)

    state.plan = build_plan(command, state)

    final_bundle = run_edde(command, state)
    final_report = final_check(command, state, final_bundle)

    if final_report.observer_status == "FALLBACK":
        state, final_bundle = apply_fallback(command, state, final_bundle)

    result = format_output(command, state, final_bundle, final_report)
    result.observer_contract = build_observer_contract(final_report)

    contract = build_edde_contract(
        command,
        state,
        final_bundle,
        result,
        result.observer_status,
        observer_contract=result.observer_contract,
        graph_snapshot=graph_summary(),
        graph_analytics=analyze_graph(limit_runs=10),
    )
    validate_edde_contract(contract)
    result.edde_contract = contract

    trace = build_trace_record(state.run_id, command, result)
    _best_effort_persist(append_trace, trace)

    SESSION_MEMORY.add_record(
        SessionRecord(
            run_id=state.run_id,
            raw_input=command.raw_input,
            intent=command.intent,
            mode=command.mode,
            summary=result.summary,
            observer_status=result.observer_status,
        )
    )

    _best_effort_persist(register_run_in_graph, state.run_id, command, result)
    _best_effort_persist(
        save_architecture_snapshot,
        str(get_checkpoint_file(state.run_id)),
        limit_runs=10,
    )

    payload = serialize_run_payload(command, result)
    _best_effort_persist(save_knowledge_object, payload)

    return result
