from __future__ import annotations

from hyperflow.metadata.worker_stubs import list_agents, list_live_worker_specs, list_worker_specs, list_workflows


def test_worker_surface_is_metadata_only() -> None:
    specs = list_worker_specs()
    assert {item['id'] for item in specs} == {
        'research-worker',
        'reasoning-worker',
        'reporting-worker',
        'tools-worker',
        'external-executor-worker',
    }
    assert all(item['integrated_with_runtime'] is False for item in specs)
    assert all(item['execution'] == 'stub.metadata_only' for item in specs)

    live_specs = list_live_worker_specs()
    workers = list_agents()
    workflows = list_workflows()
    assert len(workers) == len(specs)
    assert {item['id'] for item in live_specs} == {item['id'] for item in specs}
    assert workflows == [
        {
            'id': 'canonical-run',
            'name': 'Canonical Run',
            'description': 'Metadata-only marker for the singular runtime spine.',
            'intent': 'analysis',
            'mode': 'standard',
        }
    ]
