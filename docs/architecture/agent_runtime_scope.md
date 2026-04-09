# Hyperflow Agent Runtime — Canonical Scope

## Purpose

This document defines the controlled scope for the **agent-runtime track** above the canonical Hyperflow v0.2.0 baseline.

It answers four questions:

1. what the agent runtime is
2. what it may do
3. what it must not redefine
4. what belongs to later layers instead

The baseline remains canonical. The agent runtime is a next-layer system, not a parallel canon.

## Baseline relationship

The Hyperflow v0.2.0 baseline remains the single runtime authority underneath the agent layer.

That means:
- the baseline stays the foundation
- the canonical runtime spine stays canonical
- the agent runtime attaches above the baseline
- the agent runtime must not silently replace baseline authority

## Fixed baseline context

The following remain fixed unless challenged through an explicit canon-change proposal:

- **Hyperflow** = shell / architecture frame
- **MPS** = state-policy / mode-control layer
- **EDDE** = process execution contract
- **Observer / thresholds** = guardrail layer
- **Fragment / structured output** = output object layer

Canonical cycle:

`🌈💎🔥🧠🔀⚡`

Meaning:
- `🌈` = perceive
- `💎` = extract essence / core
- `🔥` = set direction
- `🧠` = synthesize
- `🔀` = generate / compare options
- `⚡` = choose

The agent runtime may build above this cycle, but it must not silently redefine it.

## What the agent runtime is

At this stage the agent runtime is responsible for:
- agent roles
- worker roles
- delegation logic
- coordination flow
- multi-step agent execution
- reversible workflow presets above the coordinator flow
- option generation across roles
- controlled routing above the baseline shell
- promotion-aware next-layer behavior
- explicit promotion gates for features approaching baseline relevance
- delegation-policy profiles for the agent layer only

## In scope

### 1. Agent role definition
- role purpose
- role boundaries
- role inputs and outputs
- role metadata

### 2. Delegation flow
- when delegation happens
- who delegates
- who receives
- how results return

### 3. Coordination logic
- sequencing across roles
- multi-step execution
- option generation across roles
- controlled next-action ownership

### 4. Worker execution surface
- worker metadata
- worker contracts
- worker time budgets and failure modes
- delegation-policy profiles tied to MPS-like operating modes
- worker selection logic
- lightweight execution interfaces

### 5. Promotion-aware architecture
- what could later move closer to baseline relevance
- what must remain extension-only
- what is still experimental

### 6. Guardrails for agent behavior
- invalid delegation handling
- authority-boundary protection
- drift prevention
- safe failure behavior

## Explicitly out of scope

### 1. Baseline redefinition
The agent runtime must not redefine:
- baseline authority
- canonical cycle meaning
- MPS / EDDE / Observer semantics
- the canonical runtime spine

### 2. Platform completion
The agent runtime may prepare platform needs, but it is not the platform layer itself.

### 3. Product-layer definition
The agent runtime is not responsible for product packaging, market-facing UX, or release/business framing.

### 4. Uncontrolled experimentation
Experimental ideas are allowed only when clearly labeled and separated from runtime-ready proposals.

### 5. Mythology inflation
New symbolic or conceptual complexity needs structural meaning, runtime role, and promotion criteria.

## Layer separation

### Baseline
Responsible for shell, state-policy, process contract, guardrails, and structured output contract.

### Agent runtime
Responsible for roles, delegation, coordination, worker execution surfaces, and agent-layer guardrails.

### Platform
Responsible later for operator/admin surfaces, service-level management, and wider deployment architecture.

### Product
Responsible later for user-facing packaging and delivery.

### Experimental / lab
Responsible for candidate ideas, future-layer options, and unpromoted concepts.

## Core scope rules

1. **Baseline stays canonical.**
2. **Agent runtime must be attachable.**
3. **Roles must be real.**
4. **Delegation must be real.**
5. **Promotion must be explicit.**
6. **Future layers stay separate.**

## Classification model

Every meaningful proposal in this track should be labeled as one of:
- **Baseline-safe extension**
- **Agent runtime candidate**
- **Experimental agent design**
- **Future platform candidate**
- **Product-layer candidate**
- **Out of scope**

## Current minimal runtime shape

The initial real agent-runtime surface in this repo is intentionally small:
- a coordinator role
- executable research, reasoning, tools, and reporting roles
- explicit delegation rules
- option generation across roles
- controlled choice, reporting handoff, fragment-shaped result handoff, and agent-only delegation-policy profiles
- tests that prove boundary preservation and failure behavior

This gives the project a real next layer without redefining the baseline.
