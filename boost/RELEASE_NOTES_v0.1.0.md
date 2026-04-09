# Hyperflow v0.1.0

## Overview

Hyperflow v0.1.0 is the first packaged MVP release of the project.

This release establishes the core architecture:
- emoji + text command parsing
- EDDE runtime flow
- MPS-based control
- observer validation
- structured output
- persistent trace memory
- graph memory summary
- CLI workflow

## Included in this release

### Language layer
- emoji token parsing
- intent resolution
- mode resolution
- output typing
- section-aware parsing (`Task / Goal / Format`)

### Engine layer
- runtime kernel
- planner
- reasoning
- synthesis
- fallback support

### Control layer
- MPS controller
- observer checks

### Memory layer
- session memory
- persistent traces
- knowledge store
- graph memory

### CLI
- standard JSON output
- `--pretty`
- `--save`
- `--recent`
- `--graph-summary`
- `--version`

## Validation

- test suite passing
- end-to-end CLI flow working
- GitHub repository synced

## Notes

This release is intended as:
- a stable MVP checkpoint
- a foundation for further development
- the base layer for future graph and reasoning upgrades

## Next directions

- graph visualization
- packaged distribution improvements
- richer graph analytics
- stronger output objects