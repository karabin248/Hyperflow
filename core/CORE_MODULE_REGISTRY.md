# Core Module Registry

Registry of baseline runtime modules and their current code mapping. These entries record the supported baseline surface, not speculative future expansion.

## 1) Emoji Control Stack
- **Code:** `hyperflow/language/emoji_parser.py`, `hyperflow/language/token_registry.py`, `hyperflow/language/command_builder.py`
- **Contract status:** defined baseline surface
- **Current tier:** core
- **Baseline scope:** canonical combo parsing, parser trace capture, intent/mode/output resolution

## 2) MPS Controller
- **Code:** `hyperflow/control/mps_controller.py`, `hyperflow/control/mps_profiles.py`
- **Contract status:** defined baseline surface
- **Current tier:** core
- **Baseline scope:** state-policy resolution and profile application before execution

## 3) Observer Guardrail
- **Code:** `hyperflow/control/observer.py`, `hyperflow/schemas/observer_schema.py`
- **Contract status:** defined baseline surface
- **Current tier:** core
- **Baseline scope:** pre-run checks, final checks, fallback trigger semantics

## 4) EDDE Contract Engine
- **Code:** `hyperflow/engine/edde_orchestrator.py`, `hyperflow/engine/runtime_kernel.py`
- **Contract status:** defined baseline surface
- **Current tier:** core
- **Baseline scope:** canonical execution flow and contract-backed result generation

## 5) Structured Insight Layer
- **Code:** `hyperflow/engine/synthesis.py`, `hyperflow/output/*`
- **Contract status:** defined baseline surface
- **Current tier:** core
- **Baseline scope:** fragment-oriented output construction and serialization

## 6) Runtime Knowledge / Checkpoint Layer
- **Code:** `hyperflow/checkpoint/snapshot.py`, `hyperflow/checkpoint/history.py`, `hyperflow/memory/*`
- **Contract status:** defined baseline surface
- **Current tier:** core
- **Baseline scope:** traces, graph registration, run-linked checkpoints, knowledge persistence, and read-only observability

## Promotion rule
Future-layer modules may move into `core/` only after an explicit promotion decision updates both runtime authority docs and validation coverage.
