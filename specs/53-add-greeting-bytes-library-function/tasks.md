# Tasks: Add greeting_bytes library function

**Issue**: #53
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

### T001: Add greeting_bytes and export it

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `greet` body, signature, and `ValueError("name must not be blank")` path are unchanged
- [ ] `greeting_length(name: str) -> int` body remains exactly `return len(greet(name))`
- [ ] `greeting_bytes(name: str) -> int` lives in `greet.py` immediately after `greeting_length` and is exactly `return len(greet(name).encode("utf-8"))`
- [ ] `ValueError` from `greet` is not caught or wrapped
- [ ] `from nmg_sdlc_smoke import greeting_bytes` works; `__all__ == ["greet", "greeting_length", "greeting_bytes"]`
- [ ] `src/nmg_sdlc_smoke/cli.py` is untouched
- [ ] No new runtime dependency and no new module file

**Notes**: No equivalent byte helper exists. Do not re-validate `name` in `greeting_bytes`. Keep `greeting_length` exported.

---

## Phase 2: Verification

### T002: Unit tests for greeting_bytes and unchanged greet / greeting_length

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `greeting_bytes("Ada") == 10` and `10 == len(greet("Ada").encode("utf-8"))`
- [ ] `greeting_bytes("É") == 9` and `9 == len(greet("É").encode("utf-8"))` and `9 != greeting_length("É")` and `greeting_length("É") == 8` and `9 != 10`
- [ ] parametrize blank/whitespace/non-string (`""`, `" "`, `"\\t"`, `"\\n"`, `None`, `42`) so `greeting_bytes` raises `ValueError` matching `^name must not be blank$`
- [ ] Existing `test_greet_returns_exact_message`, `test_greet_rejects_blank_and_non_string_names`, `test_greeting_length_returns_full_greeting_length`, and `test_greeting_length_rejects_blank_and_non_string_names` stay
- [ ] `tests/test_cli.py` is untouched
- [ ] `python -m pytest tests/test_greet.py tests/test_cli.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC4

**File(s)**: `tests/features/add_greeting_bytes_library_function.feature`, `tests/features/steps/test_greeting_bytes_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN004` map 1:1 to AC1–AC4
- [ ] Steps call `greet` / `greeting_length` / `greeting_bytes` in-process; CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main` with `capsys`, matching `tests/features/steps/test_greeting_length_steps.py`
- [ ] Unique `greeting_bytes` When/Then texts are implemented only in `test_greeting_bytes_steps.py`; do not add `scenarios(...)` to existing step modules
- [ ] `scenarios("../add_greeting_bytes_library_function.feature")` lives only in `test_greeting_bytes_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document greeting_bytes in README library section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing `greet("Ada")` example remains (`"Hello, Ada"`)
- [ ] Existing `greeting_length("Ada")` example remains (`10`)
- [ ] Library section shows a concise `greeting_bytes` example such as `greeting_bytes("Ada")` → `10`
- [ ] Import line includes `greeting_bytes` without dropping `greet` or `greeting_length`
- [ ] README does not hardcode a VERSION literal
- [ ] CLI section is not required to mention `greeting_bytes`

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
| #53 | 2026-09-01 | Initial feature spec |

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
