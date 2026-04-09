# MPS v5.2 Runtime Spec

Operational document for the Hyperflow core: how MPS should behave at runtime and when safety fuses should activate.

## Purpose
Define one unambiguous contract for:
- MPS levels 1–7
- Core / Satellite allocation
- Observer mode and fail-safe rules
- escalation and de-escalation decisions

## Input
- `impulse_type`: `idea | risk | decision | question | overload | strategic_signal | reset`
- `complexity_score`: `1-10`
- `stakes_score`: `1-10`
- `data_confidence`: `0.0-1.0`
- `system_load`: `low | medium | high`
- `worldcycle_phase`: `STABILIZE | EXPAND | OVERLOAD | INTEGRATE | SYNC`

## Output
- `selected_mps_level`: `1-7`
- `execution_policy`: `ZEN | CORE | DEEP | STRATEGIC | CHAOS | FUSION | HYPERFLOW`
- `observer_state`: `active | strict | recovery`
- `next_action`: `decision | map | checklist | protocol | next_step`

## MPS level contract
| Level | Name | Use case | Safety condition |
|---|---|---|---|
| 1 | ZEN | quick correction, low stakes | no escalation |
| 2 | CORE | standard analysis and one next step | default mode under uncertainty |
| 3 | DEEP | layered analysis and dependencies | medium-quality data required |
| 4 | STRATEGIC | scenarios and recommendation | cost and risk control required |
| 5 | CHAOS | controlled edge-case variants | max 5 scenarios + required integration |
| 6 | FUSION | synthesis of strategy and creativity | one stable decision core |
| 7 | HYPERFLOW | high stakes and high complexity | active observer + artifact closure |

## Core / Satellites allocation
- **Dominant Core:** 70–80% of operational energy
- **Satellites:** 10–15% each (experiment and mini-pivot)
- If satellite share exceeds 30% for 2 iterations, reduce to MPS 2

## Observer mode (fail-safe)
Observer must check:
1. false escalation
2. missing decision after 2 iterations
3. too many paths without closure
4. system overload (`worldcycle_phase=OVERLOAD`)

## Reset rule
If any condition is true:
- `system_load=high` and `data_confidence < 0.5`
- no decision after 2 iterations
- ongoing chaos without integration

then force:
- `selected_mps_level=2`
- `observer_state=recovery`
- `next_action=checklist`

## 10D decision gates (for MPS 4–7)
Decision review covers:
1. immediate goal
2. long-term goal
3. energy cost
4. system risk
5. structural / reputational impact
6. reversibility
7. worldcycle synchronization
8. impact on roles
9. impact on artifacts
10. cascade effect

## Metrics
- `% decisions closed with an artifact` (target: `>= 90%`)
- `% escalations closed with integration` (target: `>= 95%`)
- `% automatic resets to MPS2` (monitor input quality)
- `mean decision latency` per MPS level
- `observer policy error-rate`

## Failure modes
- **FM-01:** false escalation to MPS 6/7 at low stakes
  - Mitigation: force MPS 2 + one recommendation
- **FM-02:** chaos without integration
  - Mitigation: activate the reset rule and a closure checklist
- **FM-03:** satellites dilute the core
  - Mitigation: restore the 70–80% Core allocation

## Dependencies
- `hyperflow/control/mps_controller.py`
- `hyperflow/control/observer.py`
- `hyperflow/engine/edde_orchestrator.py`
- `core/CORE_QUALIFICATION_CHECKLIST.md`

## Rollback
Trigger:
- 2 consecutive iterations with FM-01 or FM-02
- or `% decisions closed with an artifact` falls below 70%

Rollback action:
- force MPS 2
- disable experimental boosters
- return to the basic EDDE + Structured Insight contract

## Tier classification
`core`
