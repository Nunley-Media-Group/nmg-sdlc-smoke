# Tasks: Add nmg-smoke --repeat COUNT option

**Issue**: #45
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

---

## Phase 1: CLI

### T001: Add argparse --repeat COUNT and print the greeting COUNT times

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `parser.add_argument("--repeat", type=_positive_count, default=1, metavar="COUNT")` is present; no short `-r`; dest remains `repeat`
- [ ] `_positive_count(value: str) -> int` lives in `cli.py`, uses `int(value)`, raises `argparse.ArgumentTypeError` on non-integer and on integers less than 1
- [ ] `parser.add_argument("name")` stays required (no `nargs="?"`)
- [ ] After successful `greet`, the CLI does `for _ in range(args.repeat): print(message)`
- [ ] `greet` is called once per successful invocation
- [ ] `ValueError` path stays `parser.exit(1, f"nmg-smoke: error: {error}\n")` with no stdout greeting
- [ ] `src/nmg_sdlc_smoke/greet.py` and `src/nmg_sdlc_smoke/__init__.py` are untouched
- [ ] No new runtime dependency

**Notes**: If `cli.py` already has `--version` or `--uppercase` from a previously delivered spec, add `--repeat` beside them and do not change those behaviors. Do not introduce a library repeat helper.

---

## Phase 2: Verification

### T002: Unit tests for --repeat and unchanged CLI

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `main(["--repeat", "3", "Ada"]) == 0` and stdout is `Hello, Ada\nHello, Ada\nHello, Ada\n` with empty stderr
- [ ] `main(["Ada", "--repeat", "3"]) == 0` and stdout is `Hello, Ada\nHello, Ada\nHello, Ada\n` with empty stderr
- [ ] `main(["--repeat", "1", "Ada"]) == 0` and stdout is `Hello, Ada\n` with empty stderr
- [ ] Existing `test_cli_prints_greeting` still expects `main(["Ada"]) == 0` and `Hello, Ada\n`
- [ ] `main(["--repeat"])` raises `SystemExit` with non-zero code and empty stdout and nonempty stderr
- [ ] `main(["--repeat", "abc", "Ada"])` raises `SystemExit` with non-zero code and empty stdout and nonempty stderr
- [ ] `main(["--repeat", "0", "Ada"])` raises `SystemExit` with non-zero code and empty stdout and nonempty stderr
- [ ] `main(["--repeat=-1", "Ada"])` raises `SystemExit` with non-zero code and empty stdout and nonempty stderr
- [ ] `main(["--repeat", "-1", "Ada"])` raises `SystemExit` with non-zero code and empty stdout
- [ ] `main(["--repeat", "2"])` raises `SystemExit` with non-zero code and empty stdout
- [ ] Parametrized blank names `""`, `" "`, `"\t"`, `"\n"` with `--repeat 2` raise `SystemExit` code `1`, empty stdout, and `name must not be blank` on stderr
- [ ] `tests/test_greet.py` is untouched
- [ ] `python -m pytest tests/test_cli.py tests/test_greet.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC6

**File(s)**: `tests/features/add_nmg_smoke_repeat_count_option.feature`, `tests/features/steps/test_repeat_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN006` map 1:1 to AC1–AC6
- [ ] Steps call `nmg_sdlc_smoke.cli.main` in-process with `capsys`, matching `tests/features/steps/test_greeting_steps.py`
- [ ] `scenarios("../add_nmg_smoke_repeat_count_option.feature")` lives only in `test_repeat_steps.py`
- [ ] New step module does not redefine step texts already defined in `test_greeting_steps.py`
- [ ] AC3 When-step runs `["--repeat"]`, `["--repeat", "abc", "Ada"]`, `["--repeat", "0", "Ada"]`, and `["--repeat", "-1", "Ada"]`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document nmg-smoke --repeat in README CLI

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] The existing `nmg-smoke Ada` / `Hello, Ada` example remains
- [ ] CLI section documents `nmg-smoke --repeat 3 Ada` printing `Hello, Ada` three times, one line each
- [ ] Library section still documents only the existing `greet` example (no repeat helper)

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
| #45 | 2026-09-01 | Initial feature spec |

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
