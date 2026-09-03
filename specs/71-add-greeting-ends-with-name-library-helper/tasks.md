# Tasks: Add greeting_ends_with_name library helper

**Issue**: #71
**Date**: 2026-09-03
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

### T001: Add greeting_ends_with_name and export it

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `greet` body, signature, and `ValueError("name must not be blank")` path are unchanged
- [ ] Existing helper bodies (`greet_many`, `greeting_length`, `greeting_bytes`, `greeting_is_ascii`, `greeting_starts_with_hello`) are unchanged
- [ ] `greeting_ends_with_name(name: str) -> bool` lives in `greet.py` immediately after `greeting_starts_with_hello` and is exactly `return greet(name).endswith(name)`
- [ ] `ValueError` from `greet` is not caught or wrapped
- [ ] `from nmg_sdlc_smoke import greeting_ends_with_name` works; `__all__` includes `"greet"`, `"greet_many"`, `"greeting_bytes"`, `"greeting_is_ascii"`, `"greeting_length"`, `"greeting_starts_with_hello"`, and `"greeting_ends_with_name"` without dropping already-exported names
- [ ] `src/nmg_sdlc_smoke/cli.py` is untouched
- [ ] `VERSION` remains `3.24.0`
- [ ] No new runtime dependency and no new module file

**Notes**: No equivalent suffix helper exists. Do not re-validate `name` in `greeting_ends_with_name`. Do not `return True`. Do not call `name.endswith(name)` without `greet`.

---

## Phase 2: Verification

### T002: Unit tests for greeting_ends_with_name and unchanged greet

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `greeting_ends_with_name("Ada") is True` and `True == greet("Ada").endswith("Ada")`
- [ ] `greeting_ends_with_name("Jo") is True` and `True == greet("Jo").endswith("Jo")` and `greet("Jo") != greet("Ada")`
- [ ] parametrize blank/whitespace/non-string (`""`, `" "`, `"\t"`, `"\n"`, `None`, `42`) so `greeting_ends_with_name` raises `ValueError` matching `^name must not be blank$`
- [ ] Existing greet and helper unit tests stay
- [ ] Import `greeting_ends_with_name` from `nmg_sdlc_smoke` without dropping existing imports
- [ ] `tests/test_cli.py` is untouched
- [ ] `python -m pytest tests/test_greet.py tests/test_cli.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC4

**File(s)**: `tests/features/add_greeting_ends_with_name_library_helper.feature`, `tests/features/steps/test_greeting_ends_with_name_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN004` map 1:1 to AC1–AC4
- [ ] Steps call `greet` / `greeting_ends_with_name` in-process; CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main` with `capsys`, matching `tests/features/steps/test_greeting_starts_with_hello_steps.py`
- [ ] Unique `greeting_ends_with_name` Given/When/Then texts are implemented only in `test_greeting_ends_with_name_steps.py`; do not add `scenarios(...)` to existing step modules
- [ ] `scenarios("../add_greeting_ends_with_name_library_helper.feature")` lives only in `test_greeting_ends_with_name_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document greeting_ends_with_name in README library section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing Library examples for `greet`, `greet_many`, `greeting_length`, `greeting_bytes`, `greeting_is_ascii`, and `greeting_starts_with_hello` remain
- [ ] Library section shows `greeting_ends_with_name("Ada")` → `True`
- [ ] Import line includes `greeting_ends_with_name` without dropping existing imported names
- [ ] README does not hardcode a VERSION literal
- [ ] CLI section is unchanged and does not mention `greeting_ends_with_name`

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
| #71 | 2026-09-03 | Initial feature spec |

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
```
