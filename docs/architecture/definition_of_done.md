# Hyperflow MVP Runtime Baseline — Definition of Done

Status: canonical
Confidence: high

## Purpose

This document defines when **Hyperflow MVP Runtime Baseline** is considered complete at the current stage.

The target is achieved only when **all** conditions below are true.

## 1. Canon is explicit

Hyperflow is clearly defined at the current stage as:

- **MVP Core**
- **Runtime Shell**
- **Minimal Orchestration Layer**

The baseline must not depend on vague, shifting, or implicit interpretations of scope.

## 2. One runtime spine exists

There is **one canonical runtime path** for:

- CLI / API entry
- parser / control interpretation
- runtime execution flow
- observer / guardrail flow
- output generation

There is no second parser, second orchestrator, second CLI authority, or parallel canonical runtime path.

## 3. The canonical cycle is locked

The canonical cycle is explicitly preserved as `🌈💎🔥🧠🔀⚡`.

Meaning:

- `🌈` = perceive
- `💎` = extract essence / core
- `🔥` = set direction
- `🧠` = synthesize
- `🔀` = generate / compare options
- `⚡` = choose

Legacy order may remain supported only for backward compatibility, but it is **not** canonical behavior.

## 4. Runtime contracts are explicit, coherent, and stable enough for the baseline

The baseline has explicit and consistent contracts for:

- parser / control behavior
- EDDE execution flow
- MPS state-policy boundaries
- observer / threshold / guardrail semantics
- output / fragment contract
- trace / checkpoint behavior

These contracts must not drift across code, docs, and tests.

## 5. Core runtime behavior is test-backed

The baseline passes its core test surface in a **clean canonical repo state**, with no unresolved known break in:

- CLI / API entry behavior
- parser behavior
- runtime kernel behavior
- persistence behavior
- contract / golden paths
- repo hygiene and packaging surface

## 6. The repository baseline is clean

The repository does not contain committed generated runtime state that should be treated as output rather than source of truth.

Examples include:

- traces
- generated graph memory payloads
- generated knowledge store payloads
- generated checkpoints
- other runtime artifact files

## 7. Docs match runtime truth

Canonical docs are aligned with implemented behavior. At minimum:

- the current runtime model is described correctly
- `README.md` does not contradict runtime truth
- canonical docs describe the real baseline, not historical intent
- key decisions are saved explicitly

## 8. The baseline is self-sufficient for the current stage

The Hyperflow baseline repo is sufficient to explain the current system stage. Other repos may exist as donor or reference material, but they are not required to understand:

- what Hyperflow is now
- how the current runtime works
- what the canonical path is
- what is core vs extension

## 9. New work mainly hardens, not redefines

Most baseline work is primarily:

- harden
- validate
- align
- freeze
- clean
- document
- guard
- minimally patch

## 10. Scope boundaries are enforceable

The project can clearly reject, defer, or redirect work that belongs to:

- full agent runtime
- platform expansion
- product packaging
- uncontrolled experimental branches

## 11. Decision logging is durable

Important changes are recorded with:

- what changed
- why it changed
- classification
- validation result
- canonical vs inferred vs deprecated vs experimental status

## 12. Future phases become separate by default

Once the above conditions are met, further work normally moves into separate tracks such as operational hardening, agent layer expansion, comparative evolution, or platform / product roadmap. Baseline-safe work may still continue for bug fixes, hygiene fixes, contract clarification, validation improvements, documentation alignment, and minimal hardening patches.

## 13. Backward compatibility is explicit

Legacy behavior may remain supported only if:

- it routes into the same canonical runtime spine
- it is labeled deprecated where appropriate
- it does not redefine canonical semantics

## Final condition

Hyperflow MVP Runtime Baseline is considered complete when it is:

- explicit in scope
- singular in runtime authority
- locked in canonical flow
- stable enough in contract
- clean in repository state
- aligned across code, docs, and tests
- durable in decision history
- resistant to scope drift
