from hyperflow.output.answer_output import AnswerOutput
from hyperflow.output.analysis_output import AnalysisOutput
from hyperflow.output.blueprint_output import BlueprintOutput
from hyperflow.output.plan_output import PlanOutput
from hyperflow.output.report_output import ReportOutput


def build_output_object(
    output_type: str,
    intent: str,
    mode: str,
    summary: str,
    confidence: str,
    observer_status: str,
    next_step: str,
    output_subtype: str = "",
    run_id: str = "",
    edde_contract: dict | None = None,
    insights: list[str] | None = None,
    actions: list[str] | None = None,
    plan: list[str] | None = None,
):
    insights = insights or []
    actions = actions or []
    plan = plan or []

    common = dict(
        intent=intent,
        mode=mode,
        summary=summary,
        confidence=confidence,
        observer_status=observer_status,
        next_step=next_step,
        output_subtype=output_subtype,
        run_id=run_id,
        insights=insights,
        actions=actions,
        plan=plan,
        edde_contract=edde_contract or {},
    )

    if output_type == "plan":
        return PlanOutput(kind="plan", **common)

    if output_type == "analysis":
        return AnalysisOutput(kind="analysis", **common)

    if output_type == "blueprint":
        return BlueprintOutput(kind="blueprint", **common)

    if output_type == "report":
        return ReportOutput(kind="report", **common)

    if output_type in {"spec", "map", "json"}:
        return AnswerOutput(kind=output_type, **common)

    return AnswerOutput(kind="answer", **common)
