# Tasks: Add nmg-smoke --version output

**Issue**: #39
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG
---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| CLI | 1 | [ ] |
| Verification | 2 | [ ] |
| Docs | 1 | [ ] |
| **Total** | 4 | |

---

## Phase 1: CLI

### T001: Add argparse --version from package metadata

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `import importlib.metadata` (or `from importlib.metadata import version`) is used; no new runtime dependency
- [ ] Parser gains `parser.add_argument("--version", action="version", version=<installed nmg-sdlc-smoke-python version>)` where the version value is `importlib.metadata.version("nmg-sdlc-smoke-python")` and is not `%(prog)s ...`
- [ ] `parser.add_argument("name")` stays required (no `nargs="?"`)
- [ ] `greet` import and blank-name `parser.exit(1, ...)` path stay
- [ ] `src/nmg_sdlc_smoke/greet.py` and `src/nmg_sdlc_smoke/__init__.py` are untouched
- [ ] No `-V` short option

**Notes**: Compute the metadata version inside `main` before `parse_args` so each invocation reads the installed distribution. argparse `action="version"` prints that string plus a newline and raises `SystemExit(0)`.

---

## Phase 2: Verification

### T002: Unit tests for version and unchanged CLI

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `main(["--version"])` raises `SystemExit` with code 0; stdout equals `importlib.metadata.version("nmg-sdlc-smoke-python") + "\n"`; stderr empty
- [ ] `main(["--version", "Ada"])` and `main(["Ada", "--version"])` each exit 0 with that same version line and no `Hello,` in stdout
- [ ] Existing `test_cli_prints_greeting` still expects `main(["Ada"]) == 0` and `Hello, Ada\n`
- [ ] `main([])` raises `SystemExit` with non-zero code and empty stdout
- [ ] `tests/test_greet.py` is untouched
- [ ] `python -m pytest tests/test_cli.py tests/test_greet.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC4

**File(s)**: `tests/features/add_nmg_smoke_version_output.feature`, `tests/features/steps/test_version_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN004` map 1:1 to AC1–AC4
- [ ] Steps call `nmg_sdlc_smoke.cli.main` in-process with `capsys`, matching `tests/features/steps/test_greeting_steps.py`
- [ ] Version assertions use `importlib.metadata.version("nmg-sdlc-smoke-python")`, not a hardcoded `3.15.0`
- [ ] `scenarios("../add_nmg_smoke_version_output.feature")` lives only in `test_version_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document nmg-smoke --version in README CLI

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] The existing `nmg-smoke Ada` / `Hello, Ada` example remains
- [ ] CLI section documents `nmg-smoke --version` as printing the installed `nmg-sdlc-smoke-python` version plus a newline and exiting 0
- [ ] README does not hardcode a VERSION literal such as `3.15.0`
- [ ] Library section still documents only `greet`

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
| #39 | 2026-08-31 | Initial feature spec |

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
