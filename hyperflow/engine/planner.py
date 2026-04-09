from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState
from hyperflow.language.section_parser import parse_sections


def build_plan(command: CommandObject, state: RuntimeState) -> list[str]:
    sections = parse_sections(command.cleaned_text)
    task = sections.get("task", "")
    goal = sections.get("goal", "")
    fmt = sections.get("format", "")

    if command.intent == "planning":
        plan = ["extract task"]

        if task:
            plan.append("identify scope")
        if goal:
            plan.append("align with goal")
        if fmt:
            plan.append("adapt to requested format")

        plan.append("order priorities")
        plan.append("synthesize final plan")
        return plan

    if command.intent == "documentation":
        plan = ["extract requirements"]
        if goal:
            plan.append("align document goal")
        if fmt:
            plan.append("shape output format")
        plan.append("structure sections")
        plan.append("finalize document")
        return plan

    if command.intent == "build":
        plan = ["identify modules"]
        if goal:
            plan.append("align build objective")
        if fmt:
            plan.append("adapt output structure")
        plan.append("define responsibilities")
        plan.append("sequence implementation")
        plan.append("finalize blueprint")
        return plan

    if command.intent == "cleanup":
        plan = ["extract noisy elements"]
        if goal:
            plan.append("preserve target core")
        plan.append("reduce redundancy")
        plan.append("finalize cleaned output")
        return plan

    plan = ["extract task", "analyze content"]
    if goal:
        plan.append("align with goal")
    if fmt:
        plan.append("adapt output structure")
    plan.append("synthesize insights")
    plan.append("finalize output")
    return plan