# Hyperflow 0.2.0 Release Notes

## Release Type
MVP stabilization release for the canonical `🌈💎🔥🧠🔀⚡` runtime line.

## What shipped
- canonical full combo locked to `🌈💎🔥🧠🔀⚡`
- direct module execution parity with `hyperflow --version`
- validated `hyperflow/edde-contract/v1` attached at runtime
- top-level `contract` exposed consistently across CLI, API, and persisted knowledge payloads
- traces now capture contract-derived phase and next-step
- one canonical contract path, output path, and run payload serializer
- repo hygiene guards against committed runtime debris
- MVP hardening for empty input, API request validation, and best-effort persistence
- package/runtime version bumped to `0.2.0`

## Install
Base runtime:
```bash
pip install -e .
```

Optional API surface:
```bash
pip install -e ".[api]"
uvicorn hyperflow.api.edde_api:create_app --factory
```

## Verification baseline
- `pytest -q`
- `hyperflow --version`
- `python -m hyperflow --version`
- `python -m hyperflow.interface.cli --version`
- canonical smoke using `🌈💎🔥🧠🔀⚡`
- `python -m hyperflow "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty`

## Known boundaries
- `experimental/` and `archive/` are outside the MVP support contract
- FastAPI support is optional and installed via the `api` extra
- the MVP promise is defined by `core/MVP_RUNTIME_FREEZE.md`

## Release packaging
- Clean source archive helper: `python scripts/make_source_zip.py`
- Default artifact name: `hyperflow-v0.2.0-source.zip`
- Archive root directory: `hyperflow-v0.2.0/`
