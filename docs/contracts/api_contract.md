# API Contract

Status: canonical
Confidence: high

## Active endpoints

The canonical MVP app exposes the following public endpoints:

- `GET /v1/health`
- `POST /v1/run`
- `GET /v1/checkpoints`
- `GET /v1/checkpoints/latest`
- `GET /v1/checkpoints/{checkpoint_id}`
- `GET /v1/logs/recent`

## FastAPI source of truth

- `hyperflow/api/edde_api.py`

## API rule

The app remains singular and exposes one runtime-backed API surface.

## Deferred to later phases

The following routes are not part of the current MVP public API:

- `DEFERRED metadata surface (removed from canonical API): GET /v1/agents`
- `DEFERRED metadata surface (removed from canonical API): GET /v1/workflows`
