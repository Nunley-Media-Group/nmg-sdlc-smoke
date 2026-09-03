# Design: Add greeting_starts_with_hello library function

**Issue**: #75
**Date**: 2026-09-03
**Status**: Approved
**Author**: NMG

---

## Overview

Add one pure function beside the existing helpers in `src/nmg_sdlc_smoke/greet.py`:

```python
def greeting_starts_with_hello(name: str) -> bool:
    return greet(name).startswith("Hello, ")
```

Export it from `src/nmg_sdlc_smoke/__init__.py` without removing any current export. Calling `greet` first preserves the exact validation and error identity. No CLI, dependency, state, storage, or version change is required.

## Architecture

The dependency direction remains caller → derived helper → `greet`. The helper adds no validation, exception handling, I/O, or state.

## API / Interface Changes

| Method | Type | Purpose |
|--------|------|---------|
| `greeting_starts_with_hello(name: str) -> bool` | Public library function | Return the current greeting's `Hello, ` prefix predicate. |

Invalid names propagate `ValueError("name must not be blank")` from `greet` unchanged.

## Alternatives Considered

| Option | Decision |
|--------|----------|
| Return `greet(name).startswith("Hello, ")` | Selected: delegates validation and reflects the greeting contract. |
| Return constant `True` | Rejected: ignores `greet` and hides future format changes. |
| Add a CLI flag | Rejected: outside the library-only scope. |

## Testing Strategy

- Unit tests for `Ada`, bool identity, export, and invalid names.
- pytest-bdd scenarios mapping AC1–AC3.
- Existing greeting and CLI tests remain unchanged and pass.
- Full pytest, feature pytest, and Ruff remain green.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Existing exports are dropped | Append the new name and assert neighboring exports. |
| Validation is duplicated or wrapped | Implement only the one-line `greet` predicate. |
| CLI behavior changes | Do not edit `cli.py`; run existing CLI coverage. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #75 | 2026-09-03 | Initial feature design |
