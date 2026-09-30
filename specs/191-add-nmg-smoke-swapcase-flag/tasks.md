# Tasks: Add nmg-smoke --swapcase flag

**Issue**: #191
**Date**: 2026-09-30
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/188-add-nmg-smoke-lowercase-flag/

## Implementation Tasks

### T001: Add the mutually exclusive --swapcase flag

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- A long-only boolean `--swapcase` is registered in the existing `case` mutually exclusive group directly after `--lowercase`; combining it with `--uppercase` or `--lowercase`, in either order, exits 2 with `not allowed with argument` on stderr and empty stdout (AC4, FR3).
- When `args.swapcase` is true, `message = message.swapcase()` runs in an `elif` branch after the `args.lowercase` check, before prefix, parentheses, braces, quotes, and the repeat/newline loop (AC1, AC2, AC3, FR1, FR2).
- Blank-name handling, default output, `--uppercase` output, `--lowercase` output, and the library API are unchanged (AC5, AC6, FR4).
- No new module, helper, or runtime dependency.

### T002: Add focused CLI unit tests

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- `main(["--swapcase", "Ada"])` and `main(["Ada", "--swapcase"])` return 0 with stdout `hELLO, aDA\n` and empty stderr (AC1).
- `main(["--swapcase", "--prefix", "OK: ", "--parentheses", "--repeat", "2", "--no-newline", "ADA"])` returns 0 with stdout `(OK: hELLO, ada)\n(OK: hELLO, ada)` and empty stderr (AC2).
- `ÅSA` → `hELLO, åsa\n` and `Straße` → `hELLO, sTRASSE\n` (AC3).
- `["--swapcase", "--uppercase", "Ada"]`, `["--uppercase", "--swapcase", "Ada"]`, `["--swapcase", "--lowercase", "Ada"]`, and `["--lowercase", "--swapcase", "Ada"]` raise `SystemExit` with code 2, empty stdout, stderr containing `not allowed with argument` (AC4).
- `--swapcase` with each of `""`, `" "`, `"\t"`, `"\n"` raises `SystemExit` code 1, empty stdout, stderr containing `name must not be blank` (AC5).
- `main(["--help"])` raises `SystemExit` code 0 and stdout contains `--swapcase` (AC6).
- `python -m pytest tests/test_cli.py` passes.

### T003: Add pytest-bdd acceptance scenarios

**File(s)**: `tests/features/add_nmg_smoke_swapcase_flag.feature`, `tests/features/steps/test_swapcase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- The feature file contains exactly the six scenarios `@SCN001`–`@SCN006` from `specs/191-add-nmg-smoke-swapcase-flag/feature.gherkin`, mapped one-to-one to AC1–AC6.
- Steps invoke the installed console script as a subprocess, resolving it with `sysconfig.get_path("scripts")` (`nmg-smoke`, falling back to `nmg-smoke.exe`) as in `tests/features/steps/test_lowercase_steps.py`, with `encoding="utf-8"` and environment `PYTHONIOENCODING=utf-8` so non-ASCII output is decoded identically on every platform.
- `python -m pytest tests/features` passes.

### T004: Document --swapcase in the README

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- The `## CLI` section, directly after the `--lowercase` documentation, documents `--swapcase` with the example `nmg-smoke --swapcase Ada` printing `hELLO, aDA`, states that case swapping uses Python `str.swapcase()` and applies before the literal prefix so prefix text keeps its original case, and states that combining `--swapcase` with `--uppercase` or `--lowercase` is rejected with exit status 2 (FR5).
- Existing CLI and library documentation is otherwise unchanged.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #191 | 2026-09-30 | Initial feature tasks |
