# Design: Add greeting_has_comma library probe

**Issue**: #113
**Date**: 2026-09-13
**Status**: Approved
**Author**: NMG

---

## Overview

Add one pure function beside the existing helpers in `src/nmg_sdlc_smoke/greet.py`:

```python
def greeting_has_comma(name: str) -> bool:
    return "," in greet(name)
```

Export it from `src/nmg_sdlc_smoke/__init__.py` without removing any current export. Calling `greet` first preserves the exact validation and error identity (`ValueError("name must not be blank")`, unwrapped). For the current default greeting, `greet("Ada")` is `Hello, Ada` and `greet("Jo")` is `Hello, Jo`; both contain the literal comma separator, so the helper returns the Python bool `True` without being hardcoded to `"Ada"`. No CLI, dependency, state, storage, or version change is required.

## Architecture

The dependency direction remains caller → derived helper → `greet`. The helper adds no validation, exception handling, I/O, or state. `src/nmg_sdlc_smoke/cli.py` is not a caller of the new helper and is not edited.

## API / Interface Changes

| Method | Type | Purpose |
|--------|------|---------|
| `greeting_has_comma(name: str) -> bool` | Public library function | Return whether `","` appears in `greet(name)`. |

Invalid names propagate `ValueError("name must not be blank")` from `greet` unchanged.

## Alternatives Considered

| Option | Decision |
|--------|----------|
| Return `"," in greet(name)` | Selected: delegates validation and reports the complete greeting’s literal comma separator. |
| Return constant `True` | Rejected: ignores `greet` and can be hardcoded to Ada. |
| Add a CLI flag | Rejected: represented only as Out of Scope outside task blocks. |

## Testing Strategy

- Unit tests in `tests/test_greet.py` for Ada, Jo (and `greet("Jo") != greet("Ada")`), bool identity, public export, and invalid names (`""`, whitespace, `None`, `42`) matching `test_greeting_starts_with_hello_*`.
- pytest-bdd feature `tests/features/add_greeting_has_comma_library_probe.feature` with `@SCN001`–`@SCN004` mapping AC1–AC4.
- Step definitions in `tests/features/steps/test_greeting_has_comma_steps.py` using the same pytest-bdd fixture/`scenarios(...)` pattern as `tests/features/steps/test_greeting_starts_with_hello_steps.py`.
- Existing greeting and CLI tests remain unchanged and pass.
- Full `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` remain green.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Existing exports are dropped | Append the new name and assert neighboring `__all__` entries. |
| Validation is duplicated or wrapped | Implement only the one-line `"," in greet(name)` predicate; assert `error.__context__ is None`. |
| CLI behavior changes | Do not edit `cli.py`; cover AC4 with existing `nmg-smoke Ada` output. |
| A TNNN is admitted without File(s) | Every `### TNNN:` heading has exactly one canonical backtick `**File(s)**` declaration; CLI exclusion is Out of Scope only. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #113 | 2026-09-13 | Initial feature design |
