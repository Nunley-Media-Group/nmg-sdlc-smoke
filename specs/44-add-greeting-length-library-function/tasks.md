# Tasks: Add greeting_length library function

**Issue**: #44
**Date**: 2026-09-01
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

### T001: Add greeting_length and export it

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `greet` body, signature, and `ValueError("name must not be blank")` path are unchanged
- [ ] `greeting_length(name: str) -> int` lives in `greet.py` immediately after `greet` and is exactly `return len(greet(name))`
- [ ] `ValueError` from `greet` is not caught or wrapped
- [ ] `from nmg_sdlc_smoke import greeting_length` works; `__all__` includes `"greet"` and `"greeting_length"` and does not drop any previously exported names
- [ ] `src/nmg_sdlc_smoke/cli.py` is untouched
- [ ] No new runtime dependency and no new module file

**Notes**: No equivalent length helper exists. Do not re-validate `name` in `greeting_length`. If `greet_many` is already exported, keep it.

---

## Phase 2: Verification

### T002: Unit tests for greeting_length and unchanged greet

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `greeting_length("Ada") == 10` and `10 == len(greet("Ada"))`
- [ ] `greeting_length("Jo") == 9` and `9 == len(greet("Jo"))` and `9 != 10`
- [ ] parametrize blank/whitespace/non-string (`""`, `" "`, `"\\t"`, `"\\n"`, `None`, `42`) so `greeting_length` raises `ValueError` matching `^name must not be blank$`
- [ ] Existing `test_greet_returns_exact_message` and `test_greet_rejects_blank_and_non_string_names` stay
- [ ] `tests/test_cli.py` is untouched
- [ ] `python -m pytest tests/test_greet.py tests/test_cli.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC4

**File(s)**: `tests/features/add_greeting_length_library_function.feature`, `tests/features/steps/test_greeting_length_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN004` map 1:1 to AC1–AC4
- [ ] Steps call `greet` / `greeting_length` in-process; CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main` with `capsys`, matching `tests/features/steps/test_greeting_steps.py`
- [ ] Do not redefine step text that already exists in `test_greeting_steps.py`; implement new unique steps in `test_greeting_length_steps.py` only
- [ ] `scenarios("../add_greeting_length_library_function.feature")` lives only in `test_greeting_length_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document greeting_length in README library section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing `from nmg_sdlc_smoke import greet` / `greet("Ada")` example remains
- [ ] Library section shows a concise `greeting_length` example such as `greeting_length("Ada")` → `10`
- [ ] README does not hardcode a VERSION literal such as `3.15.0`
- [ ] CLI section is not required to mention `greeting_length`

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
| #44 | 2026-09-01 | Initial feature spec |

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
