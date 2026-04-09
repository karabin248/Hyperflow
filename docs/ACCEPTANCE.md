# ACCEPTANCE CRITERIA — Hyperflow MVP v0.3.0

## Definition of Done

### Core Engine
- [x] EDDE pipeline runs: Extract → Discover → Do → Evaluate
- [x] LLM (OpenRouter) called in Do phase when backend is set
- [x] Stub fallback when LLM unavailable
- [x] MPS levels 1–7 applied correctly
- [x] Observer contract attached to every run result

### API
- [x] `POST /v1/run` returns structured JSON
- [x] `GET /v1/logs/recent` returns last N log entries
- [x] `POST /v1/repositories/scan` validates URL scheme

### Testing
- [x] All unit tests pass with asyncio.run() wrappers
- [x] Mock LLM backend unified in conftest.py
- [x] Log store isolated between test runs

### Security
- [x] URL validation before git clone (SSRF prevention)
- [x] LLM errors captured in typed schema field

### Packaging
- [x] `pip install -e .[test]` succeeds
- [x] Makefile targets: install, test, check, clean
