from hyperflow.engine.runtime_kernel import run
from hyperflow.language.command_builder import build_command
from hyperflow.schemas.edde_contract_schema import validate_edde_contract

PROMPT_MATRIX = [
    ("🌈💎🔥🧠🔀⚡ Write a function that adds two numbers", "build", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a function that checks for a palindrome", "build", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a simple function that sorts a list of numbers", "build", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a definition of entropy in simple words", "documentation", "spec"),
    ("🌈💎🔥🧠🔀⚡ Write a short history of artificial intelligence", "documentation", "spec"),
    ("🌈💎🔥🧠🔀⚡ Create a list of 5 questions for a math quiz", "planning", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a guide for beginner programmers", "documentation", "spec"),
    ("🌈💎🔥🧠🔀⚡ Write a simple algorithm that calculates factorial", "build", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Explain the difference between AI and ML", "documentation", "spec"),
    ("🌈💎🔥🧠🔀⚡ Create a list of 3 examples of AI use in medicine", "planning", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a short calculator instruction guide", "documentation", "spec"),
    ("🌈💎🔥🧠🔀⚡ Create a simple program that calculates the average of a list", "build", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a mini-essay about the meaning of entropy in physics", "documentation", "spec"),
    ("🌈💎🔥🧠🔀⚡ Generate a list of 5 mindfulness tips", "planning", "blueprint"),
    ("🌈💎🔥🧠🔀⚡ Write a function that converts degrees C -> F", "build", "blueprint"),
]


def test_prompt_matrix_builds_commands_and_contracts():
    for prompt, expected_intent, expected_output in PROMPT_MATRIX:
        command = build_command(prompt)
        result = run(command)
        contract = getattr(result, "edde_contract", {})

        assert command.tokens[:6] == ["🌈", "💎", "🔥", "🧠", "🔀", "⚡"]
        assert command.mode == "fusion"
        assert command.intent == expected_intent
        assert command.output_type == expected_output
        assert command.operations == ["perceive", "extract_core", "set_direction", "synthesize", "generate_options", "choose"]
        validate_edde_contract(contract)
        assert contract["output"]["kind"] == expected_output
        assert contract["timeline"][0]["next_step"] == "DO"
        assert contract["timeline"][-1]["next_step"] in {"DECIDE", "END"}
