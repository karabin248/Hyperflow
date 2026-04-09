# Hyperflow Runtime Contract

Status: canonical
Confidence: high

## Purpose

This document defines the **current runtime contract** for Hyperflow MVP Runtime Baseline across code, docs, tests, and project decisions.

## Contract scope

This contract applies to the canonical baseline runtime, including:

- CLI entry
- module entry
- API entry
- parser / control interpretation
- runtime execution flow
- observer / guardrail flow
- output generation
- trace / checkpoint behavior

It does not define future platform or product behavior.

## Canonical runtime authority

There must be one canonical runtime spine.

### Canonical runtime path

CLI / API entry → command construction → runtime_kernel.run() → output / persistence

No second parser, second orchestrator, second CLI authority, or parallel canonical runtime path should be introduced. The parser resolution policy is `longest_match_first`.

## Canonical entrypoints

The baseline exposes stable canonical entrypoints for CLI, module execution, and API surface. These entrypoints must route into the same canonical runtime spine, and `/v1/run` is the only canonical runtime endpoint. Additional convenience paths must not redefine runtime authority.

## Parser / control contract

The parser/control layer must provide explicit and stable interpretation of the canonical cycle `🌈💎🔥🧠🔀⚡`.

### Canonical semantic mapping

- `🌈` → `perceive`
- `💎` → `extract_core`
- `🔥` → `set_direction`
- `🧠` → `synthesize`
- `🔀` → `generate_options`
- `⚡` → `choose`

### Required parser behavior

The parser/control layer must:

- interpret canonical control inputs consistently
- preserve canonical cycle order
- avoid conflicting alternate meanings inside the baseline
- route legacy order only as backward compatibility, not as canon

### Legacy compatibility rule

The legacy cycle `🌈💎🔥🧠⚡🔀` may remain supported only if:

- it resolves into the same runtime spine
- it is treated as **deprecated** / non-canonical
- it does not redefine canonical semantics

## MPS state-policy contract

MPS defines the state-policy / mode-control layer of the runtime. At baseline level, this contract requires:

- explicit state-policy role
- stable mode-control behavior
- no drift into second orchestration authority
- no confusion between MPS policy and EDDE execution flow

MPS is responsible for mode selection, transition policy, and state boundaries. It is not a full orchestration engine, product workflow engine, or platform layer.

## EDDE execution contract

EDDE defines the process execution contract of the runtime. At baseline level, EDDE must provide:

- explicit runtime phase logic
- coherent sequencing
- stable relation to parser/control interpretation
- stable relation to runtime kernel execution

## Observer / guardrail contract

The observer / guardrail layer exists to prevent runtime drift and unsafe or incoherent state transitions. At baseline level it must provide:

- explicit threshold / guardrail meaning
- stable relation to runtime flow
- protection against silent drift
- rollback-safe behavior where applicable

## Output / fragment contract

The output layer must produce structured runtime results coherent with the canonical baseline. At minimum the contract requires:

- stable output shape
- explicit final result behavior
- compatibility with fragment / structured output expectations
- no contradiction between runtime result and canonical docs

Output generation must remain downstream of the canonical runtime spine.

## Trace / checkpoint / persistence contract

Runtime traces, checkpoints, and other persistence artifacts are **runtime outputs**, not baseline source truth. Generated runtime artifacts must not be treated as canonical source material inside the baseline repo.

Examples include:

- traces
- generated graph memory payloads
- generated knowledge store payloads
- generated checkpoints
- similar runtime output files

The canonical repo baseline must remain clean, and repo hygiene tests must enforce this.

## Test contract

The runtime contract is not considered valid unless it is test-backed. Parser / control, baseline action routing, baseline action execution helpers, MPS, and output contract behavior must qualify through `make baseline-qualify`. At minimum the baseline test surface must cover:

- CLI behavior
- API behavior
- parser/control behavior
- runtime kernel behavior
- persistence behavior
- contract/golden flows
- repo hygiene
- packaging/source-zip integrity

## Docs alignment contract

Runtime docs must align with implemented behavior. At minimum:

- `README.md` must not contradict runtime truth
- canonical docs must describe the actual baseline
- historical/archive material must not pose as current runtime authority
- key contract decisions must be saved explicitly

## Baseline change rules

### Allowed baseline-safe changes

- bug fixes
- hygiene fixes
- validation strengthening
- contract clarification
- documentation alignment
- minimal hardening patches

### Disallowed baseline changes by default

- second runtime spine
- parallel canonical parser
- second orchestration authority
- uncontrolled semantic redefinition
- scope inflation into platform/product layers

## Contract status labels

All important runtime decisions should be labeled as one of:

- **Canonical**
- **Confirmed**
- **Inferred**
- **Deprecated**
- **Experimental**

## Final runtime contract statement

Hyperflow MVP Runtime Baseline is contract-stable when:

- the runtime spine is singular
- the canonical cycle is preserved
- parser/control semantics are coherent
- MPS and EDDE boundaries are explicit enough for the baseline
- guardrails support runtime stability
- output behavior is structured and aligned
- persistence artifacts are treated as generated outputs, not source truth
- tests, docs, and code agree on the same runtime model
