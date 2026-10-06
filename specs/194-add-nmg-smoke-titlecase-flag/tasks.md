# Tasks: Add nmg-smoke --titlecase flag

**Issue**: #194
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/191-add-nmg-smoke-swapcase-flag/

## Implementation Tasks

### T001: Add the mutually exclusive --titlecase flag

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- A long-only boolean `--titlecase` is registered in the existing `case` mutually exclusive group directly after `--swapcase`; combining it with `--uppercase`, `--lowercase`, or `--swapcase`, in either order, exits 2 with `not allowed with argument` on stderr and empty stdout (AC4, FR3).
- When `args.titlecase` is true, `message = message.title()` runs in an `elif` branch after the `args.swapcase` check, before prefix, parentheses, braces, quotes, and the repeat/newline loop (AC1, AC2, AC3, FR1, FR2).
- Blank-name handling, default output, `--uppercase`, `--lowercase`, and `--swapcase` output, and the library API are unchanged (AC5, AC6, FR4).
- No new module, helper, or runtime dependency.

### T002: Add focused CLI unit tests

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- `main(["--titlecase", "ada"])` and `main(["ada", "--titlecase"])` return 0 with stdout `Hello, Ada\n` and empty stderr (AC1).
- `"ADA LOVELACE"` → `Hello, Ada Lovelace\n`, `"o'neil"` → `Hello, O'Neil\n`, and `"åsa"` → `Hello, Åsa\n`, each returning 0 (AC2).
- `main(["--titlecase", "--prefix", "ok: ", "--quotes", "--repeat", "2", "--no-newline", "ADA"])` returns 0 with stdout `"ok: Hello, Ada"\n"ok: Hello, Ada"` and empty stderr (AC3).
- `["--titlecase", "--uppercase", "Ada"]`, `["--uppercase", "--titlecase", "Ada"]`, `["--titlecase", "--lowercase", "Ada"]`, `["--lowercase", "--titlecase", "Ada"]`, `["--titlecase", "--swapcase", "Ada"]`, and `["--swapcase", "--titlecase", "Ada"]` raise `SystemExit` with code 2, empty stdout, stderr containing `not allowed with argument` (AC4).
- `--titlecase` with each of `""`, `" "`, `"\t"`, `"\n"` raises `SystemExit` code 1, empty stdout, stderr containing `name must not be blank` (AC5).
- `main(["--help"])` raises `SystemExit` code 0 and stdout contains `--titlecase` (AC6).
- `python -m pytest tests/test_cli.py` passes.

### T003: Add pytest-bdd acceptance scenarios

**File(s)**: `tests/features/add_nmg_smoke_titlecase_flag.feature`, `tests/features/steps/test_titlecase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- The feature file contains exactly the six scenarios `@SCN001`–`@SCN006` from `specs/194-add-nmg-smoke-titlecase-flag/feature.gherkin`, mapped one-to-one to AC1–AC6.
- Steps invoke the installed console script as a subprocess, resolving it with `sysconfig.get_path("scripts")` (`nmg-smoke`, falling back to `nmg-smoke.exe`) as in `tests/features/steps/test_swapcase_steps.py`, with `encoding="utf-8"` and environment `PYTHONIOENCODING=utf-8` so non-ASCII output is decoded identically on every platform.
- `python -m pytest tests/features` passes.

### T004: Document --titlecase in the README

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- The `## CLI` section, directly after the `--swapcase` documentation, documents `--titlecase` with the example `nmg-smoke --titlecase ada` printing `Hello, Ada`, states that title-casing uses Python `str.title()` and applies before the literal prefix so prefix text keeps its original case, and states that combining `--titlecase` with `--uppercase`, `--lowercase`, or `--swapcase` is rejected with exit status 2 (FR5).
- Existing CLI and library documentation is otherwise unchanged.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #194 | 2026-10-06 | Initial feature tasks |
