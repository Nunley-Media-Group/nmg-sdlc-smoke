# Design: Add greeting_ends_with_exclamation library function

**Issue**: #79
**Date**: 2026-09-04
**Status**: Approved
**Author**: NMG

---

## Overview

Add one pure function beside the existing helpers in `src/nmg_sdlc_smoke/greet.py`:

```python
def greeting_ends_with_exclamation(name: str) -> str:
    return f"{greet(name)}!"
```

Export it from `src/nmg_sdlc_smoke/__init__.py` without removing current exports. Calling `greet` preserves its exact validation contract. No CLI, dependency, state, storage, or version change is required.

## Architecture

Dependency direction remains caller → derived helper → `greet`. The helper adds no validation, exception handling, I/O, or state.

## API Change

| Method | Type | Purpose |
|--------|------|---------|
| `greeting_ends_with_exclamation(name: str) -> str` | Public library function | Return the current greeting followed by exactly one exclamation mark. |

## Testing Strategy

- Unit tests cover public import, exact output, whitespace preservation, and invalid names.
- pytest-bdd scenarios map AC1–AC4.
- Existing greeting and CLI tests remain green.
- Full pytest, feature pytest, and Ruff pass.

## Risks and Mitigations

| Risk | Mitigation |
|------|------------|
| Validation diverges | Delegate directly to `greet`. |
| Existing exports are dropped | Append the export and retain existing names. |
| CLI behavior changes | Do not edit `cli.py`; run its regression tests. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #79 | 2026-09-04 | Initial feature design |
