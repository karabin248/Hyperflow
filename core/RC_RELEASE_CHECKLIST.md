# RC Release Checklist

## Purpose
Define the minimum release-candidate checks for the Hyperflow `0.2.0` MVP line.

## Packaging
- [ ] `python3 -m pip install -e .`
- [ ] `python3 -m pip install -e ".[api]"`
- [ ] `python3 -m pip install -e ".[test]"`

## Version / Entrypoints
- [ ] `hyperflow --version` returns `Hyperflow 0.2.0`
- [ ] `python -m hyperflow --version` returns `Hyperflow 0.2.0`
- [ ] `python -m hyperflow.interface.cli --version` returns `Hyperflow 0.2.0`

## Canonical Runtime Smoke
- [ ] `hyperflow "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty`
- [ ] `python -m hyperflow "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty`
- [ ] `python -m hyperflow.interface.cli "🌈💎🔥🧠🔀⚡ Task: build a deployment plan" --pretty`

## API Smoke
- [ ] `uvicorn hyperflow.api.edde_api:create_app --factory`
- [ ] `GET /health` returns `{"status":"ok","service":"hyperflow"}`
- [ ] `POST /v1/run` returns top-level `run_id` and `contract`

## Contract / Payload Freeze
- [ ] `pytest -q hyperflow/tests/test_contract_golden.py`
- [ ] `pytest -q hyperflow/tests/test_run_payload_golden.py`
- [ ] `pytest -q hyperflow/tests/test_packaging_metadata.py`

## Repo Hygiene
- [ ] no committed `storage/*` payloads
- [ ] no committed `__pycache__/`, `.pytest_cache/`, or `*.egg-info/`
- [ ] `python scripts/make_source_zip.py` succeeds and writes `hyperflow-v0.2.0-source.zip` containing `hyperflow-v0.2.0/`
- [ ] release zip excludes runtime debris and VCS internals
