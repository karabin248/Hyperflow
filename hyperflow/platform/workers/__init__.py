"""Deferred worker surface markers.

This deferred donor/product surface exposes only worker_handlers metadata helpers.
register_default_workers remains a no-op placeholder until an explicit promotion decision.
"""

from hyperflow.metadata.worker_stubs import list_live_worker_specs

worker_handlers: dict[str, object] = {}


def register_default_workers() -> None:
    return None
