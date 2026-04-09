# AUTHORITY MAP

## Active Runtime Spine
- `hyperflow/engine/runtime_kernel.py` — async execution orchestrator
- `hyperflow/engine/edde_orchestrator.py` — EDDE pipeline
- `hyperflow/engine/reasoning.py` — phase implementations
- `hyperflow/language/command_builder.py` — parser authority
- `hyperflow/language/emoji_parser.py` — emoji authority

## Archive / Generated Outputs
- `artifacts/` — build outputs, not part of active spine
- `dist/`, `build/`, `*.egg-info` — generated, gitignored

## Deferred / Future Layers
- `hyperflow/extensions/` — not yet promoted to active spine
- `hyperflow/metadata/worker_stubs.py` — stub, not live

## Test Authority
- `tests/` — canonical test suite
- `tests_base/` — base classification tests
- `tests_integration/` — integration smoke tests
