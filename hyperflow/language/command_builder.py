from hyperflow.language.action_router import route_emoji_actions
from hyperflow.language.emoji_parser import extract_tokens, parse_emoji_controls, strip_tokens
from hyperflow.language.intent_resolver import resolve_intent, resolve_operations
from hyperflow.language.mode_resolver import (
    resolve_constraints,
    resolve_intensity,
    resolve_mode,
)
from hyperflow.language.output_typer import resolve_output_type, resolve_output_subtype
from hyperflow.language.section_parser import parse_sections
from hyperflow.schemas.command_schema import CommandObject


def _resolve_confidence(
    tokens: list[str],
    sections: dict,
    intent: str,
    output_type: str,
    parser_trace: dict,
) -> str:
    score = 0

    if tokens:
        score += 1
    if sections.get("task"):
        score += 2
    elif sections.get("body"):
        score += 1

    if intent != "unknown":
        score += 1

    if output_type != "answer":
        score += 1

    if sections.get("goal"):
        score += 1

    if parser_trace.get("matched_combo") or parser_trace.get("matched_preset"):
        score += 1

    if score >= 5:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def build_command(raw_input: str) -> CommandObject:
    raw_input = str(raw_input or "").strip()
    if not raw_input:
        raise ValueError("Input is required.")

    parser_trace = parse_emoji_controls(raw_input)
    action_route_trace = route_emoji_actions(raw_input)
    parser_trace["action_routes"] = action_route_trace.get("matched", [])
    parser_trace["action_route_errors"] = action_route_trace.get("errors", [])
    tokens = parser_trace.get("tokens") or extract_tokens(raw_input)
    cleaned_text = strip_tokens(raw_input, tokens, parser_trace.get("matched_sequences", []))
    sections = parse_sections(cleaned_text)

    source_text = sections.get("task") or sections.get("body") or cleaned_text

    intent = resolve_intent(tokens, source_text, parser_trace)
    operations = resolve_operations(tokens, source_text, parser_trace)
    mode = resolve_mode(tokens, cleaned_text, parser_trace)
    intensity = resolve_intensity(tokens)
    constraints = resolve_constraints(tokens, cleaned_text)

    output_source = " ".join(
        part
        for part in [
            sections.get("task", ""),
            sections.get("goal", ""),
            sections.get("format", ""),
            cleaned_text,
        ]
        if part
    )
    output_type = resolve_output_type(output_source, parser_trace)
    output_subtype = resolve_output_subtype(output_source, output_type, parser_trace)

    priority = "high" if intensity in {"high", "boosted"} else "normal"
    confidence = _resolve_confidence(tokens, sections, intent, output_type, parser_trace)

    return CommandObject(
        raw_input=raw_input,
        cleaned_text=cleaned_text,
        tokens=tokens,
        intent=intent,
        mode=mode,
        operations=operations,
        constraints=constraints,
        output_type=output_type,
        output_subtype=output_subtype,
        intensity=intensity,
        priority=priority,
        confidence=confidence,
        parser_trace=parser_trace,
        action_routes=action_route_trace.get("matched", []),
    )
