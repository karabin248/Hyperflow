from hyperflow.extensions.emoji_action_router import route_emoji_actions
from hyperflow.language.command_builder import build_command


def test_route_simple_inline_path_argument() -> None:
    routed = route_emoji_actions("📁 ./data/input.csv")

    assert routed["errors"] == []
    assert routed["matched"][0]["action_id"] == "data.load"
    assert routed["matched"][0]["arguments"]["path"] == "./data/input.csv"


def test_route_goal_arguments_with_regex_capture() -> None:
    routed = route_emoji_actions("🎯 accuracy 0.95")

    assert routed["errors"] == []
    assert routed["matched"][0]["arguments"] == {"kpi": "accuracy", "value": "0.95"}


def test_route_multi_emoji_sequence_preserves_order() -> None:
    routed = route_emoji_actions("🤖🧠🔍📸")

    assert [item["action_id"] for item in routed["matched"]] == [
        "agent.run_main",
        "reason.invoke_deep",
        "debug.trace",
        "snapshot.save",
    ]


def test_build_command_persists_action_routes_in_parser_trace() -> None:
    command = build_command("📁 ./data/input.csv")

    assert command.action_routes
    assert command.parser_trace["action_routes"][0]["action_id"] == "data.load"
    assert command.parser_trace["action_routes"][0]["arguments"]["path"] == "./data/input.csv"


def test_route_canonical_full_combo_prefers_longest_match() -> None:
    routed = route_emoji_actions("🌈💎🔥🧠🔀⚡ Write a plan")

    assert routed["errors"] == []
    assert [item["emoji"] for item in routed["matched"]] == ["🌈💎🔥🧠🔀⚡"]
    assert routed["matched"][0]["action_id"] == "pipeline.canonical_full"



def test_route_goal_target_only_sets_target_without_errors() -> None:
    routed = route_emoji_actions("🎯 repo-alpha 💎")

    assert routed["errors"] == []
    assert routed["matched"][0]["target"] == "repo-alpha"
    assert routed["matched"][0]["arguments"]["target"] == "repo-alpha"


def test_route_diamond_inline_target_from_braces() -> None:
    routed = route_emoji_actions("💎{repo-alpha}")

    assert routed["errors"] == []
    assert routed["matched"][0]["emoji"] == "💎"
    assert routed["matched"][0]["target"] == "repo-alpha"


def test_route_diamond_inline_target_from_index_syntax() -> None:
    routed = route_emoji_actions("💎[2]")

    assert routed["errors"] == []
    assert routed["matched"][0]["target"] == "2"
