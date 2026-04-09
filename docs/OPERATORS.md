# OPERATORS GUIDE

## Running Hyperflow

### Install
```bash
pip install -e .[test]
# or
make install
```

### CLI
```bash
python -m hyperflow "🌈💎🔥🧠🔀⚡ analyze global architecture"
python -m hyperflow --json "plan the migration strategy"
python -m hyperflow --pretty "generate a factorial function"
```

### API (FastAPI)
```bash
uvicorn main:app --reload
# POST /v1/run  {"input": "your prompt"}
```

### Module Entrypoint
```bash
python -m hyperflow.run "your prompt"
```

## Versioned Source ZIP
```bash
python scripts/make_source_zip.py
```
