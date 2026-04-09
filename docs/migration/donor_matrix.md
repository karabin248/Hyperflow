# Donor Matrix

| Repo | Role | PR-01 decision | Confidence |
|---|---|---|---|
| `hyperflow-step57-source-zip-script-root-version-fixed` | canonical runtime seed | use as base | high |
| `hyperflow-platform-canonical-1` | product-surface donor | defer ingestion | high |
| `hyperflow-v0.2.0-source` | packaging / CI donor | salvage minimal deltas | high |
| `hyperflow-0.1.1-v0.1.2-workstream-source-zip-root-fixed-1-1` | config / contract oracle donor | document guidance only | medium |
| `hyperflow-emoji-action-router` | regression donor | defer to later tests | high |
| `hyperflow-merged-repo` | historical / selective donor only | not a base | high |

## PR-01 application

Applied donor deltas in this PR:

- `hyperflow-v0.2.0-source`: add `httpx` to test extras, align workflow naming to `ci.yml`

Deferred donor deltas:

- platform routes and models
- config-order code changes
- parser/router regression imports
- selective rescue from `hyperflow-merged-repo`


## PR follow-up status
- Canonical `/v1/run` contract remains owned by `hyperflow.api.edde_api` and `hyperflow.output.run_payload`.
- Product inventory surface is absorbed under `hyperflow.api` and `hyperflow.platform` only.
- `GET /v1/checkpoints` and `GET /v1/logs/recent` are surfaced in the canonical MVP app without introducing a second runtime root. `GET /v1/agents` and `GET /v1/workflows` remain deferred donor/product surface.


- `hyperflow-platform-canonical-1` now also donates the Android shell under `apps/android/`.
- `hyperflow-platform-canonical-1` worker files were absorbed as metadata/stubs under `hyperflow/platform/workers/`.
