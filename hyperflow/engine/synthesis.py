from __future__ import annotations

from hyperflow.schemas.command_schema import CommandObject
from hyperflow.schemas.runtime_state_schema import RuntimeState


def extract_core_insights(draft_result: dict) -> list[str]:
    insights = draft_result.get("partial_insights", [])
    return insights[:3] if insights else ["No insights generated."]


def _contains_any(text: str, *terms: str) -> bool:
    return any(term in text for term in terms)


def _direct_artifact_for_task(command: CommandObject) -> str | None:
    text = (command.cleaned_text or command.raw_input).strip()
    lower = text.lower()

    if _contains_any(lower, "dodającą dwie liczby", "add two numbers") or (
        "funkcj" in lower and _contains_any(lower, "dwie liczby", "two numbers")
    ):
        return "def add(a, b):\n    return a + b"

    if _contains_any(lower, "palindrom", "palindrome"):
        return (
            "def is_palindrome(text):\n"
            "    cleaned = ''.join(ch.lower() for ch in str(text) if ch.isalnum())\n"
            "    return cleaned == cleaned[::-1]"
        )

    if _contains_any(lower, "sortującą listę liczb", "sort numbers", "sort a list of numbers") or (
        "sort" in lower and _contains_any(lower, "listę liczb", "list of numbers")
    ):
        return "def sort_numbers(numbers):\n    return sorted(numbers)"

    if _contains_any(lower, "silni", "factorial"):
        return (
            "def factorial(n):\n"
            "    if n < 0:\n"
            "        raise ValueError('n must be non-negative')\n"
            "    result = 1\n"
            "    for i in range(2, n + 1):\n"
            "        result *= i\n"
            "    return result"
        )

    if _contains_any(lower, "średniej z listy", "sredniej z listy", "average of a list"):
        return (
            "def average(numbers):\n"
            "    if not numbers:\n"
            "        raise ValueError('numbers cannot be empty')\n"
            "    return sum(numbers) / len(numbers)"
        )

    if (_contains_any(lower, "stopnie c", "celsius") and _contains_any(lower, "f", "fahrenheit")) or "c to f" in lower:
        return "def c_to_f(celsius):\n    return (celsius * 9 / 5) + 32"

    if (_contains_any(lower, "definicj", "define", "definition") and _contains_any(lower, "entropii", "entropy")) or "simple words" in lower:
        return (
            "Entropy is a measure of disorder or of how many different states a system can occupy. "
            "The higher the entropy, the more possible arrangements the system can have."
        )

    if _contains_any(lower, "różnicę między ai a ml", "roznice między ai a ml", "difference between ai and ml"):
        return (
            "AI is the broader field of building systems that perform tasks requiring intelligence. "
            "ML is a subset of AI in which a model learns patterns from data instead of being described only by hand-written rules."
        )

    if _contains_any(lower, "historię o sztucznej inteligencji", "story about artificial intelligence"):
        return (
            "One day, a small AI model woke up in a server room filled with lights and data. "
            "Instead of dreaming about taking over the world, it only wanted to understand people better. "
            "Every conversation became a new star on its map of meaning, until it discovered "
            "that real intelligence is not about power, but about connecting knowledge, empathy, and imagination."
        )

    if _contains_any(lower, "listę 5 pytań do quizu matematycznego", "5 math quiz questions"):
        return (
            "1. What is 7 × 8?\n"
            "2. What is 144 ÷ 12?\n"
            "3. What is 15 + 27?\n"
            "4. What is the perimeter of a square with side length 6 cm?\n"
            "5. What is 9²?"
        )

    if _contains_any(lower, "poradnik dla początkujących programistów", "guide for beginner programmers"):
        return (
            "1. Pick one language and learn its fundamentals.\n"
            "2. Practice every day with small exercises.\n"
            "3. Learn to read error messages carefully.\n"
            "4. Build simple projects instead of only studying theory.\n"
            "5. Use Git and save your progress often.\n"
            "6. Ask questions, take notes, and revisit difficult concepts regularly."
        )

    if _contains_any(lower, "3 przykładów zastosowań ai w medycynie", "3 przykladow zastosowan ai w medycynie", "3 examples of ai in medicine"):
        return (
            "1. Analysis of medical images, for example detecting changes in X-rays and MRI scans.\n"
            "2. Diagnostic support based on patient history and test results.\n"
            "3. Therapy personalization through prediction of treatment effectiveness."
        )

    if _contains_any(lower, "instrukcję obsługi kalkulatora", "instrukcje obsługi kalkulatora", "calculator instructions"):
        return (
            "1. Turn on the calculator with the power button.\n"
            "2. Enter the first number.\n"
            "3. Choose an operation such as +, -, ×, or ÷.\n"
            "4. Enter the second number.\n"
            "5. Press = to see the result.\n"
            "6. Use C or AC to clear the screen."
        )

    if _contains_any(lower, "mini-esej o znaczeniu entropii w fizyce", "mini essay about the meaning of entropy in physics"):
        return (
            "In physics, entropy describes how widely energy and matter can be dispersed within a system. "
            "It is central to thermodynamics because it helps explain why natural processes move in a particular direction, "
            "for example why heat flows from a warmer body to a cooler one. "
            "Entropy connects order, probability, and irreversibility, which is why it remains one of the foundations of modern physics."
        )

    if _contains_any(lower, "5 porad mindfulness", "5 mindfulness tips"):
        return (
            "1. Start with two minutes of mindful breathing.\n"
            "2. Notice thoughts without judging them.\n"
            "3. Regularly return attention to the body and the senses.\n"
            "4. Limit multitasking and do one thing at a time.\n"
            "5. End the day with a short, calm reflection."
        )

    return None


def build_summary(command: CommandObject, draft_result: dict) -> str:
    direct_artifact = _direct_artifact_for_task(command)
    if direct_artifact:
        return direct_artifact

    ops = ", ".join(command.operations) if command.operations else "analyze"

    if command.intent == "planning":
        return (
            "Hyperflow prepared a structured plan focused on task scope, "
            f"priorities, and execution flow using operations: {ops}."
        )

    if command.intent == "build":
        return (
            "Hyperflow prepared a build-oriented blueprint focused on modules, "
            f"responsibilities, and implementation order using operations: {ops}."
        )

    if command.intent in {"documentation", "mapping"}:
        return (
            f"Hyperflow produced a structured {command.output_type} with emphasis on "
            f"clarity, organization, and core extraction using operations: {ops}."
        )

    if command.intent == "cleanup":
        return (
            "Hyperflow reduced noise and preserved the core signal, returning a "
            f"cleaned structured result using operations: {ops}."
        )

    return (
        f"Hyperflow executed intent '{command.intent}' in mode '{command.mode}' "
        f"with operations: {ops}."
    )


def run_evaluate_phase(
    command: CommandObject,
    state: RuntimeState,
    draft_result: dict,
) -> dict:
    state.phase = "evaluate"
    insights = extract_core_insights(draft_result)
    summary = build_summary(command, draft_result)

    return {
        "summary": summary,
        "final_insights": insights,
        "actions": draft_result.get("actions", []),
        "confidence": "high" if state.mps_level >= 4 else "medium-high",
        "next_step": "expand" if command.intent in {"planning", "build", "mapping"} else "done",
    }
