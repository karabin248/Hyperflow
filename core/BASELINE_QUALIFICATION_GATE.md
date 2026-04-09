# Baseline Qualification Gate

Status: canonical
Confidence: high

Hyperflow baseline canon is frozen behind this rule:

> No new canonical behavior may emerge outside the baseline qualification gate.

## Baseline authority at this stage

Hyperflow baseline is the:

- runtime shell
- reasoning authority
- control authority

The attached extension layers may harden, validate, or review behavior above the baseline, but they do not define canonical runtime behavior unless promoted explicitly.

## What this gate protects

The gate protects the canonical baseline for:

- Hyperflow runtime shell
- EDDE execution contract
- MPS state-policy / mode-control layer
- parser/control language
- output contract
- core trace / core checkpoint truth

## Qualification command

```bash
make baseline-qualify
```

Underlying entrypoint:

```bash
bash scripts/baseline_qualification.sh
```

## Required evidence

The gate must keep proving that:

- canonical entrypoints do not import `hyperflow.framework`
- canonical entrypoints do not import `hyperflow.agent_runtime`
- canonical schema validation does not depend on future layers
- CLI and API still route through the same runtime kernel authority
- core trace / checkpoint modules remain future-layer free
- canonical observability routes stay baseline-backed
- parser/control semantics stay baseline-owned
- baseline action routing stays baseline-owned
- baseline action execution helpers stay baseline-owned
- MPS mode-control semantics stay baseline-owned
- output contract semantics stay baseline-owned
- EDDE / output / checkpoint behavior remains baseline-backed
- canonical trace/checkpoint truth path singular
- deferred inventory and worker metadata surfaces remain non-canonical
- release verification still passes from the canonical baseline

## Promotion boundary

Framework, agent-runtime, platform, and worker metadata layers may produce stronger review evidence, but they must not become canonical by narrative, proximity, or convenience.

Promotion remains explicit.
