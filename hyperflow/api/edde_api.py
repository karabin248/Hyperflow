from __future__ import annotations

from typing import Any

from hyperflow.runtime_kernel import run
from hyperflow.output.run_payload import serialize_run_payload
from hyperflow.language.command_builder import build_command
from hyperflow.version import get_version

try:
    from fastapi import FastAPI, HTTPException
except ModuleNotFoundError:  # pragma: no cover - optional dependency bridge
    FastAPI = None
    HTTPException = RuntimeError

from hyperflow.api.models import HealthResponse, RunRequest, RunResponse


def create_app() -> Any:
    if FastAPI is None:
        raise ModuleNotFoundError("FastAPI is required to create the Hyperflow API app")

    from hyperflow.api.routes_checkpoints import router as checkpoints_router
    from hyperflow.api.routes_logs import router as logs_router

    # NOTE: The agents and workflows route modules are DEFERRED donor/product surfaces.
    # They are NOT mounted in the canonical MVP app.  See docs/architecture/authority_map.md
    # and docs/contracts/api_contract.md.  Mount them only after an explicit promotion decision.

    app = FastAPI(title="Hyperflow API", version=get_version())

    def _health_payload() -> dict[str, str]:
        return {"status": "ok", "service": "hyperflow", "version": get_version()}

    @app.get("/v1/health", response_model=HealthResponse)
    def health() -> dict[str, str]:
        return _health_payload()

    @app.get("/health", response_model=HealthResponse)
    def health_legacy_alias() -> dict[str, str]:
        return _health_payload()

    @app.post("/v1/run", response_model=RunResponse)
    def run_flow(request: RunRequest) -> RunResponse:
        try:
            command = build_command(request.prompt)
            result = run(command)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        except Exception as exc:  # pragma: no cover - defensive API wrapper
            raise HTTPException(status_code=500, detail=f"runtime_error: {exc}") from exc

        payload = serialize_run_payload(command, result)
        return RunResponse(
            run_id=payload["run_id"],
            intent=payload["intent"],
            mode=payload["mode"],
            output_type=payload["output_type"],
            result=payload["result"],
            contract=payload["contract"],
        )

    app.include_router(checkpoints_router)
    app.include_router(logs_router)
    return app


app = create_app() if FastAPI is not None else None
