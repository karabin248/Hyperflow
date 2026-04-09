from hyperflow.output.base import BaseOutput
from hyperflow.output.factory import build_output_object
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.observer_schema import ObserverReport
from hyperflow.schemas.runtime_state_schema import RuntimeState


def format_output(
    command: CommandObject,
    state: RuntimeState,
    final_bundle: dict,
    observer_report: ObserverReport,
) -> BaseOutput:
    confidence = final_bundle.get("confidence", command.confidence)
    if observer_report.confidence_adjustment == "down":
        if confidence == "medium-high":
            confidence = "medium"
        elif confidence == "medium":
            confidence = "low-medium"

    return build_output_object(
        output_type=command.output_type,
        intent=command.intent,
        mode=command.mode,
        summary=final_bundle.get("summary", ""),
        confidence=confidence,
        observer_status=observer_report.observer_status,
        next_step=final_bundle.get("next_step", ""),
        output_subtype=command.output_subtype,
        insights=final_bundle.get("final_insights", []),
        actions=final_bundle.get("actions", []),
        plan=state.plan,
        run_id=state.run_id,
    )
