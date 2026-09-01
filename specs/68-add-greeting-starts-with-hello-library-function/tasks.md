# Tasks: Add greeting_starts_with_hello library function

**Issue**: #68
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

### T001: Add greeting_starts_with_hello and export it

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `greet` body, signature, and `ValueError("name must not be blank")` path are unchanged
- [ ] `greeting_length(name: str) -> int` body remains exactly `return len(greet(name))`
- [ ] `greeting_is_ascii(name: str) -> bool` body remains exactly `return greet(name).isascii()`
- [ ] `greeting_starts_with_hello(name: str) -> bool` lives in `greet.py` immediately after `greeting_is_ascii` (or after `greeting_contains_name` / `greeting_bytes` if that function already exists) and is exactly `return greet(name).startswith("Hello, ")`
- [ ] `ValueError` from `greet` is not caught or wrapped
- [ ] `from nmg_sdlc_smoke import greeting_starts_with_hello` works; `__all__` includes `"greet"`, `"greeting_is_ascii"`, `"greeting_length"`, and `"greeting_starts_with_hello"` without dropping already-exported names
- [ ] `src/nmg_sdlc_smoke/cli.py` is untouched
- [ ] No new runtime dependency and no new module file

**Notes**: No equivalent prefix helper exists. Do not re-validate `name` in `greeting_starts_with_hello`. Do not `return True`. Do not call `name.startswith("Hello, ")`. Keep `greeting_length` and `greeting_is_ascii` exported.

---

## Phase 2: Verification

### T002: Unit tests for greeting_starts_with_hello and unchanged greet / helpers

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `greeting_starts_with_hello("Ada") is True` and `True == greet("Ada").startswith("Hello, ")`
- [ ] `greeting_starts_with_hello("Jo") is True` and `True == greet("Jo").startswith("Hello, ")` and `greet("Jo") != greet("Ada")`
- [ ] parametrize blank/whitespace/non-string (`""`, `" "`, `"\\t"`, `"\\n"`, `None`, `42`) so `greeting_starts_with_hello` raises `ValueError` matching `^name must not be blank$`
- [ ] Existing `test_greet_returns_exact_message`, `test_greet_rejects_blank_and_non_string_names`, `test_greeting_length_returns_full_greeting_length`, `test_greeting_length_rejects_blank_and_non_string_names`, `test_greeting_is_ascii_returns_true_for_ascii_greeting`, `test_greeting_is_ascii_returns_false_for_non_ascii_greeting`, and `test_greeting_is_ascii_rejects_blank_and_non_string_names` stay
- [ ] `tests/test_cli.py` is untouched
- [ ] `python -m pytest tests/test_greet.py tests/test_cli.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC4

**File(s)**: `tests/features/add_greeting_starts_with_hello_library_function.feature`, `tests/features/steps/test_greeting_starts_with_hello_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN004` map 1:1 to AC1–AC4
- [ ] Steps call `greet` / `greeting_starts_with_hello` in-process; CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main` with `capsys`, matching `tests/features/steps/test_greeting_is_ascii_steps.py`
- [ ] Unique `greeting_starts_with_hello` When/Then texts are implemented only in `test_greeting_starts_with_hello_steps.py`; do not add `scenarios(...)` to existing step modules
- [ ] `scenarios("../add_greeting_starts_with_hello_library_function.feature")` lives only in `test_greeting_starts_with_hello_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document greeting_starts_with_hello in README library section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing `greet("Ada")` example remains (`"Hello, Ada"`)
- [ ] Existing `greeting_length("Ada")` example remains (`10`)
- [ ] Existing `greeting_is_ascii("Ada")` example remains (`True`)
- [ ] Library section shows a concise `greeting_starts_with_hello` example such as `greeting_starts_with_hello("Ada")` → `True`
- [ ] Import line includes `greeting_starts_with_hello` without dropping `greet`, `greeting_is_ascii`, or `greeting_length`
- [ ] README does not hardcode a VERSION literal
- [ ] CLI section is not required to mention `greeting_starts_with_hello`

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
| #68 | 2026-09-01 | Initial feature spec |

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
