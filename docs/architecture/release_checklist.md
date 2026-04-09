# Release checklist

Use this checklist before cutting a new MVP artifact:

1. `pip install -e ".[api,test]"`
2. `pytest -q hyperflow/tests tests --ignore=hyperflow/tests/test_built_sdist_smoke.py --ignore=hyperflow/tests/test_built_wheel_smoke.py`
3. `make packaging-smoke`
4. `python -m build --sdist --wheel --no-isolation`
5. verify `hyperflow --version`
6. verify `python -m hyperflow --version`
7. verify `/health`, `/v1/run`, `/v1/checkpoints`, `/v1/checkpoints/latest`, `/v1/logs/recent`
8. verify `/v1/agents` and `/v1/workflows` are not part of the public MVP API
9. confirm packaged configs and `runtime_contract_health_check.json` are present in built artifacts
