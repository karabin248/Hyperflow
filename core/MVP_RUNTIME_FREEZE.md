# MVP Runtime Freeze

## Purpose
Define the supported Hyperflow MVP runtime surface for the `0.2.0` release line.

## Canonical Path
`🌈💎🔥🧠🔀⚡` is the only documented canonical full-combo route.

## Frozen Execution Spine
1. `hyperflow.language.command_builder.build_command()`
2. `hyperflow.engine.runtime_kernel.run()`
3. `hyperflow.output.edde_contract.build_edde_contract()`
4. `hyperflow.schemas.edde_contract_schema.validate_edde_contract()`
5. `hyperflow.output.run_payload.serialize_run_payload()`

## Frozen Interface Surface
- CLI: `hyperflow.interface.cli:main`
- Package module entrypoint: `python -m hyperflow`
- Direct CLI module entrypoint: `python -m hyperflow.interface.cli`
- API: `hyperflow.api.edde_api:create_app` and `/v1/run`

## Frozen Payload Contract
Top-level run payload fields:
- `command`
- `intent`
- `mode`
- `output_type`
- `result`
- `run_id`
- `contract`

## Frozen EDDE Contract
- schema: `hyperflow/edde-contract/v1`
- phases: `DECIDE -> DO -> OUTPUT`
- runtime sections: `pipeline_path`, `pipeline_stage_map`, `mps`, `graph`

## MVP Hardening Rules
- persistence writes for traces, graph registration, and knowledge storage are best-effort and must not break a successful run
- CLI save failures must terminate with a user-facing error instead of a traceback-only failure
- empty input is invalid at the command-builder and interface layer

## Explicitly Out of Scope
- alternate top-level runtimes
- experimental combo variants as canonical behavior
- documentation in `archive/` or `experimental/` as release truth

## Packaging Boundary
- base install: `pip install -e .`
- optional API install: `pip install -e ".[api]"`
- release smoke must cover both console-script and module-entrypoint version checks
