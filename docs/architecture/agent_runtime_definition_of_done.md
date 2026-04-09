# Hyperflow Agent Runtime — Definition of Done

The agent runtime is considered stage-complete only when all of the following are true.

## 1. Baseline authority remains intact
- the baseline stays the single runtime authority underneath the agent layer
- the agent runtime does not replace the canonical runtime spine
- the agent layer attaches above the baseline instead of forking it

## 2. Agent-runtime scope is explicit
The runtime is clearly responsible for:
- agent roles
- agent execution boundaries
- task delegation
- coordination logic
- multi-step execution across agents
- option generation across agents
- reversible workflow presets above the coordinator flow
- promotion-aware extension behavior

## 3. Agent roles are explicit
Each role has:
- a clear purpose
- an execution boundary
- clear inputs
- clear outputs
- a clear relationship to baseline authority

## 4. Delegation logic is real
At minimum delegation has:
- explicit trigger conditions
- defined task handoff structure
- controlled execution path
- clear result return path

## 5. Coordination flow exists
The runtime demonstrates:
- sequencing across roles
- controlled coordination logic
- no ambiguity about next-action ownership
- stable relation to the baseline spine

## 6. Canonical baseline semantics are preserved
The canonical cycle remains `🌈💎🔥🧠🔀⚡` and retains its fixed meanings.

## 7. Agent-layer boundaries are documented
It is clear what belongs to:
- baseline
- agent runtime
- future platform layer
- product layer
- experimental layer

## 8. Runtime contracts are explicit
Contracts exist for:
- agent role behavior
- handoff behavior
- execution sequencing
- result return behavior
- failure / guardrail behavior
- worker metadata and execution descriptors
- explicit worker `time_budget_ms` and `failure_modes`
- fragment-shaped handoff behavior for runtime results
- delegation-policy profiles tied to MPS-like operating modes for the agent layer only

## 9. Guardrails exist for agent behavior
At minimum:
- invalid delegation is rejected or safely handled
- agent drift cannot silently redefine authority
- coordination failures are observable

## 10. Test-backed behavior exists
Validation covers:
- role selection or routing
- delegation flow
- coordination path
- worker execution surface
- worker failure/time-budget handling
- delegation-profile enforcement and profile-specific option flow
- failure handling
- boundary preservation

## 11. It is attachable and reversible
The agent runtime can be removed or delayed without breaking baseline usefulness.

## 12. It does not force platform assumptions too early
The agent runtime may prepare future platform logic, but it makes sense on its own.

## 13. Promotion criteria are explicit
Promotion requires:
- runtime usefulness
- test-backed stability
- reversible integration
- explicit contracts
- no baseline-authority drift

## 14. Decision logging is durable
Important decisions record:
- what changed
- why it changed
- classification
- validation result
- promotion status or criteria

## 15. The layer is operationally usable
The architecture is understandable, execution is real, boundaries are explicit, and validation is honest.
