# Tasks: Add nmg-smoke --no-newline flag

**Issue**: #58
**Date**: 2026-09-01
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

**Steering alignment**: This CLI-only change follows the registered managed steering runtime in `steering/manifest.json`; it adds no project-specific validation declaration or steering artifact change.

---

## Phase 1: CLI

### T001: Add --no-newline and preserve repeated separators

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `parser.add_argument("--no-newline", action="store_true")` is present; there is no short `-n` and no value-taking configuration
- [ ] `parser.add_argument("name")` stays required
- [ ] Existing `--uppercase`, `--repeat COUNT`, and `--prefix TEXT` parser declarations and transform order remain
- [ ] `greet(args.name)` is still called exactly once before any stdout output
- [ ] Existing `ValueError` handling stays `parser.exit(1, f"nmg-smoke: error: {error}\n")`
- [ ] The existing print loop becomes `for index in range(args.repeat)` and sets `end = "" if args.no_newline and index == args.repeat - 1 else "\n"` before `print(message, end=end)`
- [ ] The implementation does not build a repeated list or joined output string and does not import `sys`
- [ ] `src/nmg_sdlc_smoke/greet.py` and `src/nmg_sdlc_smoke/__init__.py` are untouched
- [ ] No runtime dependency, new module, or VERSION change

**Notes**: Empty `end` applies only to the final iteration when flagged. Earlier repetitions keep `
` separators. Prefix and uppercase already form `message` before the output loop and remain unchanged.

---

## Phase 2: Verification

### T002: Unit tests for --no-newline and unchanged failures

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Parametrize `main(["--no-newline", "Ada"])` and `main(["Ada", "--no-newline"])`; both return 0 with stdout exactly `Hello, Ada` and empty stderr
- [ ] Existing `test_cli_prints_greeting` still expects `main(["Ada"]) == 0` and `Hello, Ada
`
- [ ] `main(["--no-newline", "--repeat", "3", "Ada"])` returns 0 with stdout exactly `Hello, Ada
Hello, Ada
Hello, Ada`
- [ ] `main(["--no-newline", "--repeat", "1", "Ada"])` matches the single flagged invocation
- [ ] `main(["--no-newline", "--uppercase", "Ada"])` returns 0 with stdout exactly `HELLO, ADA`
- [ ] `main(["--no-newline"])` raises `SystemExit` with non-zero code, empty stdout, and argparse stderr
- [ ] Parametrized blank names `""`, `" "`, `"\t"`, and `"\n"` with `--no-newline` raise `SystemExit` code 1, leave stdout empty, and include `name must not be blank` on stderr
- [ ] Existing uppercase, repeat, prefix, and invalid-repeat tests remain without weakened expectations
- [ ] `tests/test_greet.py` is untouched
- [ ] `python -m pytest tests/test_cli.py tests/test_greet.py` exits 0

### T003: Add pytest-bdd feature and no-newline steps

**File(s)**: `tests/features/add_nmg_smoke_no_newline_flag.feature`, `tests/features/steps/test_no_newline_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec metadata header
- [ ] Scenarios `@SCN001` through `@SCN007` map 1:1 to AC1 through AC7
- [ ] Steps call `nmg_sdlc_smoke.cli.main` in-process with `capsys`; no subprocess or installed-binary dependency
- [ ] `scenarios("../add_nmg_smoke_no_newline_flag.feature")` lives only in `test_no_newline_steps.py`
- [ ] `pytest_plugins = ["test_greeting_steps", "test_uppercase_steps", "test_repeat_steps"]` reuses existing shared steps without redefining them
- [ ] Exact stdout assertions distinguish `Hello, Ada` from `Hello, Ada
` and preserve the two inter-greeting newlines for repeat 3
- [ ] AC7 directly verifies `greet("Ada")`, `greeting_length("Ada")`, and the existing invalid-name `ValueError` contract
- [ ] Existing feature and step modules are unchanged
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document --no-newline in README CLI section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing `nmg-smoke Ada`, `--uppercase`, `--repeat COUNT`, and `--prefix TEXT` CLI examples remain
- [ ] CLI documentation states that `nmg-smoke --no-newline Ada` writes `Hello, Ada` without a trailing newline
- [ ] Library section is unchanged
- [ ] README does not hardcode a VERSION literal

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
| #58 | 2026-09-01 | Initial feature spec |

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
