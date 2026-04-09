from __future__ import annotations

from hyperflow.config import get_mps_regulator_config
from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.observer_schema import ObserverReport
from hyperflow.schemas.runtime_state_schema import RuntimeState

_PLANNING_HINTS = ("plan", "checklist", "roadmap", "lista", "checklista")
_BUILD_HINTS = ("build", "module", "repo", "zbuduj")


def _safe_reroute_action(default: str = "fallback") -> str:
    safe_reroute = get_mps_regulator_config().get("safe_reroute", {})
    return str(safe_reroute.get("strategy", default))


def _threshold_status(issues: list[str], *, hard_fail: bool = False) -> tuple[str, str]:
    if hard_fail:
        return "FAIL", "hard_guardrail_triggered"
    if issues:
        return "FAIL", "threshold_breached"
    return "OK", "within_threshold"


def build_observer_contract(report: ObserverReport) -> dict[str, str | list[str]]:
    return {
        "status": report.threshold_status,
        "observer_status": report.observer_status,
        "reason": report.threshold_reason,
        "issues": list(report.issues),
        "recommended_action": report.recommended_action,
    }


def pre_run_check(command: CommandObject) -> ObserverReport:
    issues: list[str] = []

    if command.intent == "unknown":
        issues.append("unknown_intent")

    if not command.cleaned_text and not command.tokens:
        issues.append("empty_input")

    lower = command.cleaned_text.lower()
    if command.output_type == "answer" and any(term in lower for term in _PLANNING_HINTS):
        issues.append("possible_output_type_mismatch")

    threshold_status, threshold_reason = _threshold_status(issues)
    if issues:
        return ObserverReport(
            observer_status="WARN",
            issues=issues,
            recommended_action="clarify_or_continue",
            confidence_adjustment="down",
            threshold_status=threshold_status,
            threshold_reason=threshold_reason,
        )

    return ObserverReport(threshold_status=threshold_status, threshold_reason=threshold_reason)


def final_check(
    command: CommandObject,
    state: RuntimeState,
    final_bundle: dict,
) -> ObserverReport:
    issues: list[str] = []

    summary = final_bundle.get("summary", "").strip()
    insights = final_bundle.get("final_insights", [])
    actions = final_bundle.get("actions", [])
    confidence = str(final_bundle.get("confidence", command.confidence))
    lower_summary = summary.lower()

    if not summary:
        issues.append("missing_summary")

    if not insights:
        issues.append("missing_insights")

    if command.output_type == "plan" and not state.plan:
        issues.append("missing_plan")

    if command.intent == "planning" and not any(term in lower_summary for term in _PLANNING_HINTS + ("steps", "structured")):
        issues.append("summary_not_plan_oriented")

    if command.intent == "build" and not any(term in lower_summary for term in _BUILD_HINTS):
        issues.append("summary_not_build_oriented")

    if not actions:
        issues.append("missing_actions")

    if state.mps_level >= 5 and len(insights) < 2:
        issues.append("high_mps_needs_more_signal")

    if state.mps_level >= 6 and confidence in {"low", "low-medium"}:
        issues.append("satellite_ops_low_confidence")

    hard_fail = "missing_summary" in issues or "missing_plan" in issues
    threshold_status, threshold_reason = _threshold_status(issues, hard_fail=hard_fail)

    if hard_fail:
        return ObserverReport(
            observer_status="FALLBACK",
            issues=issues,
            recommended_action=_safe_reroute_action(),
            confidence_adjustment="down",
            threshold_status=threshold_status,
            threshold_reason=threshold_reason,
        )

    if issues:
        return ObserverReport(
            observer_status="WARN",
            issues=issues,
            recommended_action="continue_with_warning",
            confidence_adjustment="down",
            threshold_status=threshold_status,
            threshold_reason=threshold_reason,
        )

    return ObserverReport(threshold_status=threshold_status, threshold_reason=threshold_reason)
