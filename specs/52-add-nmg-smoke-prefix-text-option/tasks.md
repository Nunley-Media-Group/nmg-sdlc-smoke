# Tasks: Add nmg-smoke --prefix TEXT option

**Issue**: #52
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

### T001: Add argparse --prefix TEXT and prepend it after uppercase

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `parser.add_argument("--prefix", default="", metavar="TEXT")` is present; no short `-p`; dest remains `prefix`
- [ ] `parser.add_argument("name")` stays required (no `nargs="?"`)
- [ ] `--prefix` does not use `nargs="?"` (bare `--prefix` must fail argparse)
- [ ] After successful `greet` and the existing `if args.uppercase: message = message.upper()` block, the CLI does `message = args.prefix + message` then `for _ in range(args.repeat): print(message)`
- [ ] `greet` is still called once per successful invocation
- [ ] `ValueError` path stays `parser.exit(1, f"nmg-smoke: error: {error}\n")` with no stdout greeting
- [ ] Existing `--uppercase` and `--repeat` arguments stay; their parsers are not rewritten
- [ ] `src/nmg_sdlc_smoke/greet.py` and `src/nmg_sdlc_smoke/__init__.py` are untouched
- [ ] No new runtime dependency

**Notes**: Concatenate with `+`; do not add a separator. Empty default `""` makes omit and empty TEXT share the current stdout. Do not introduce a library prefix helper.

---

## Phase 2: Verification

### T002: Unit tests for --prefix and unchanged CLI

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `main(["--prefix", "OK: ", "Ada"]) == 0` and stdout is `OK: Hello, Ada\n` with empty stderr
- [ ] `main(["Ada", "--prefix", "OK: "]) == 0` and stdout is `OK: Hello, Ada\n` with empty stderr
- [ ] Existing `test_cli_prints_greeting` still expects `main(["Ada"]) == 0` and `Hello, Ada\n`
- [ ] `main(["--prefix", "", "Ada"]) == 0` and stdout is `Hello, Ada\n` with empty stderr
- [ ] `main(["--prefix"])` raises `SystemExit` with non-zero code and empty stdout and nonempty stderr that contains `usage:` or `error:`
- [ ] `main(["--prefix", "OK: "])` raises `SystemExit` with non-zero code and empty stdout
- [ ] Parametrized blank names `""`, `" "`, `"\t"`, `"\n"` with `--prefix` TEXT `OK: ` raise `SystemExit` code `1`, empty stdout, and `name must not be blank` on stderr
- [ ] `main(["--prefix", "OK: ", "--uppercase", "Ada"]) == 0` and stdout is `OK: HELLO, ADA\n` with empty stderr
- [ ] `main(["--prefix", "OK: ", "--repeat", "2", "Ada"]) == 0` and stdout is `OK: Hello, Ada\nOK: Hello, Ada\n` with empty stderr
- [ ] Existing uppercase and repeat unit tests remain passing without expectation changes
- [ ] `tests/test_greet.py` is untouched
- [ ] `python -m pytest tests/test_cli.py tests/test_greet.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC7

**File(s)**: `tests/features/add_nmg_smoke_prefix_text_option.feature`, `tests/features/steps/test_prefix_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN007` map 1:1 to AC1–AC7
- [ ] Steps call `nmg_sdlc_smoke.cli.main` in-process with `capsys`, matching `tests/features/steps/test_greeting_steps.py`
- [ ] `scenarios("../add_nmg_smoke_prefix_text_option.feature")` lives only in `test_prefix_steps.py`
- [ ] `pytest_plugins = ["test_greeting_steps", "test_uppercase_steps", "test_repeat_steps"]`
- [ ] New step module does not redefine step texts already defined in those plugins
- [ ] AC3 When-step runs `["--prefix"]`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document nmg-smoke --prefix in README CLI

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] The existing `nmg-smoke Ada` / `Hello, Ada` example remains
- [ ] Existing `--uppercase` and `--repeat` CLI examples remain
- [ ] CLI section documents `nmg-smoke --prefix 'OK: ' Ada` printing `OK: Hello, Ada`
- [ ] Library section still documents only `greet` and `greeting_length` (no prefix helper)

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
| #52 | 2026-09-01 | Initial feature spec |

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
