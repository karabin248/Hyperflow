# Hyperflow merge checklist

## Base repository
- [x] Keep `hyperflow-main` as the canonical runtime spine.
- [x] Avoid importing Repo A's parallel CLI/runtime shell.

## Phase 1 completed
- [x] Added machine-data sample fixture: `examples/data/sales_data.csv`
- [x] Added data-ingest toolset under `hyperflow/framework/tools/data_ingest.py`
- [x] Added machine-metadata summarizer tool
- [x] Added optional FastAPI surface under `hyperflow/api/edde_api.py`
- [x] Added tests for workflow-based data ingest and API health/run flow

## Next merge steps
- [ ] Bridge data tools into the live EDDE runtime path
- [ ] Add optional IP Guardian extension under `hyperflow/extensions/ip_guardian/`
- [ ] Add config loader for `edde-core.json` and `mps-regulator.json`
- [ ] Attach fragment persistence to data/profile outputs
- [ ] Add dependency extras for `api` and richer ingest connectors
