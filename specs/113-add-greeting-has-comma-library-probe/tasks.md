# Tasks: Add greeting_has_comma library probe

**Issue**: #113
**Date**: 2026-09-13
**Status**: Approved
**Author**: NMG

---

## Summary

| Task | Description | Status |
|------|-------------|--------|
| T001 | Add and export the pure helper | [ ] |
| T002 | Add unit and BDD coverage | [ ] |
| T003 | Document the library probe | [ ] |

The installed candidate admits every `### TNNN:` heading when taskIds is omitted. Each of T001–T003 has exactly one canonical `**File(s)**` declaration of repository-relative backtick paths. Do not add an excluded or no-op TNNN without `File(s)`. No CLI work is a task; it is only the Out of Scope bullet in requirements.md.

### T001: Add and export greeting_has_comma

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `greeting_has_comma(name: str) -> bool` is implemented as `return "," in greet(name)`.
- [ ] `greeting_has_comma("Ada")` is `True` and equals `"," in greet("Ada")`.
- [ ] `greeting_has_comma("Jo")` is `True`, equals `"," in greet("Jo")`, and `greet("Jo") != greet("Ada")`.
- [ ] Blank, whitespace-only, and non-string names raise `ValueError("name must not be blank")` from `greet` with no wrapping.
- [ ] `from nmg_sdlc_smoke import greeting_has_comma` works; existing `__all__` names remain.
- [ ] `greet` and `src/nmg_sdlc_smoke/cli.py` are not edited.

### T002: Add unit and BDD coverage

**File(s)**: `tests/test_greet.py`, `tests/features/add_greeting_has_comma_library_probe.feature`, `tests/features/steps/test_greeting_has_comma_steps.py`
**Type**: Modify and Create
**Depends**: T001
**Acceptance**:
- [ ] Unit tests cover AC1–AC4 observables: Ada, Jo not hardcoded, invalid-name error identity, public export, and unchanged `greet("Ada")`.
- [ ] Feature file defines `@SCN001`–`@SCN004` mapping AC1–AC4 with Given/When/Then.
- [ ] Step definitions bind that feature via pytest-bdd `scenarios(...)` using the existing helper-step pattern.
- [ ] Existing greeting and CLI regressions still pass.

### T003: Document the library probe

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001, T002
**Acceptance**:
- [ ] README Library import list includes `greeting_has_comma`.
- [ ] README includes `greeting_has_comma("Ada")  # True` in the library example block.
- [ ] CLI documentation under `## CLI` is unchanged.
- [ ] Zero new runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` all pass.

Delivery evidence must explain alignment with `steering/manifest.json` and its registered managed steering runtime.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #113 | 2026-09-13 | Initial feature task plan |
