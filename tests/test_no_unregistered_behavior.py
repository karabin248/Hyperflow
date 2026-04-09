from __future__ import annotations

from hyperflow.contracts.runtime_invariants import assert_behavior_registered, get_registered_behavior_ids
from hyperflow.language.action_router import route_emoji_actions
from hyperflow.language.command_builder import build_command


def test_every_routed_action_is_registered() -> None:
    command = build_command('🌈💎🔥🧠🔀⚡ 📁 ./data/input.csv 📊 create a rollout plan')
    action_ids = [route['action_id'] for route in command.parser_trace.get('action_routes', [])]
    assert action_ids
    for action_id in action_ids:
        assert assert_behavior_registered(action_id) == action_id


def test_behavior_registry_blocks_unregistered_ids() -> None:
    registered = get_registered_behavior_ids()
    assert 'pipeline.canonical_full' in registered
    try:
        assert_behavior_registered('pipeline.shadow_runtime')
    except ValueError as exc:
        assert 'Unregistered behavior detected' in str(exc)
    else:
        raise AssertionError('expected ValueError for unregistered behavior')


def test_router_outputs_no_wild_behavior_ids() -> None:
    routed = route_emoji_actions('🌈💎🔥🧠🔀⚡ 📊, 📁 ./data/input.csv')
    registered = get_registered_behavior_ids()
    observed = {item['action_id'] for item in routed['matched']}
    assert observed <= registered
