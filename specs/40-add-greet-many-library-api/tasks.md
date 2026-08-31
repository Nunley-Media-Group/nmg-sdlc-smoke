# Tasks: Add greet_many library API

**Issue**: #40
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG
---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| Library | 1 | [ ] |
| Verification | 2 | [ ] |
| Docs | 1 | [ ] |
| **Total** | 4 | |

---

## Phase 1: Library

### T001: Add greet_many and export it

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `greet` body, signature, and `ValueError("name must not be blank")` path are unchanged
- [ ] `greet_many(names: Iterable[str]) -> list[str]` lives in `greet.py`; import `Iterable` from `collections.abc`
- [ ] Bare `str` raises `TypeError("names must not be a str")` before iteration
- [ ] Valid iterables return `[greet(name) for name in names]`; empty iterable returns `[]`
- [ ] `ValueError` from `greet` is not caught or wrapped
- [ ] `from nmg_sdlc_smoke import greet_many` works; `__all__ == ["greet", "greet_many"]`
- [ ] `src/nmg_sdlc_smoke/cli.py` is untouched
- [ ] No new runtime dependency and no new module file

**Notes**: No equivalent batch helper exists. Do not special-case `bytes` / `bytearray`. Non-iterable `names` may raise the interpreter's `TypeError`.

---

## Phase 2: Verification

### T002: Unit tests for greet_many and unchanged greet

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `greet_many(["Ada", "Bob"]) == ["Hello, Ada", "Hello, Bob"]`
- [ ] `greet_many(["Ada", "Ada"]) == ["Hello, Ada", "Hello, Ada"]`
- [ ] `greet_many([]) == []`; also empty tuple and empty generator return `[]`
- [ ] tuple `("Ada", "Bob")` and generator `n for n in ["Ada", "Bob"]` return the same two-element list
- [ ] `greet_many(["Ada", " ", "Bob"])` and `greet_many(["", "Bob"])` and a non-string first-invalid element each raise `ValueError` matching `^name must not be blank$` (no returned list)
- [ ] `greet_many("Ada")` raises `TypeError` and does not return `["Hello, A", "Hello, d", "Hello, a"]`
- [ ] Existing `test_greet_returns_exact_message` and `test_greet_rejects_blank_and_non_string_names` stay
- [ ] `tests/test_cli.py` is untouched
- [ ] `python -m pytest tests/test_greet.py tests/test_cli.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC5

**File(s)**: `tests/features/add_greet_many_library_api.feature`, `tests/features/steps/test_greet_many_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN005` map 1:1 to AC1–AC5
- [ ] Steps call `greet` / `greet_many` in-process; CLI assertions in AC5 call `nmg_sdlc_smoke.cli.main` with `capsys`, matching `tests/features/steps/test_greeting_steps.py`
- [ ] Do not redefine step text that already exists in `test_greeting_steps.py`; implement new unique steps in `test_greet_many_steps.py` only
- [ ] `scenarios("../add_greet_many_library_api.feature")` lives only in `test_greet_many_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document greet_many in README library section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing `from nmg_sdlc_smoke import greet` / `greet("Ada")` example remains
- [ ] Library section shows a concise `greet_many` example such as `greet_many(["Ada", "Bob"])` → `["Hello, Ada", "Hello, Bob"]`
- [ ] README does not hardcode a VERSION literal such as `3.15.0`
- [ ] CLI section is not required to mention `greet_many`

---

## Dependency Graph

```
T001 ──┬──▶ T002 ──▶ T003
       └──▶ T004
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #40 | 2026-08-31 | Initial feature spec |

---

## Validation Checklist

Before moving to IMPLEMENT phase:

- [x] Each task has single responsibility
- [x] Dependencies are correctly mapped
- [x] Tasks can be completed independently (given dependencies)
- [x] Acceptance criteria are verifiable
- [x] File paths reference actual project structure
- [x] Test tasks are included
- [x] No circular dependencies
- [x] Tasks are in logical execution order
