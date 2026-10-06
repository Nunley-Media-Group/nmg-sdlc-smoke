# Tasks: Add nmg-smoke --casefold flag

**Issue**: #197
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/194-add-nmg-smoke-titlecase-flag/

## Implementation Tasks

### T001: Add the mutually exclusive --casefold flag

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- A long-only boolean `--casefold` is registered in the existing `case` mutually exclusive group directly after `--titlecase`; combining it with `--uppercase`, `--lowercase`, `--swapcase`, or `--titlecase`, in either order, exits 2 with `not allowed with argument` on stderr and empty stdout (AC4, FR3).
- When `args.casefold` is true, `message = message.casefold()` runs in an `elif` branch after the `args.titlecase` check, before prefix, parentheses, braces, quotes, and the repeat/newline loop (AC1, AC2, AC3, FR1, FR2).
- Blank-name handling, default output, `--uppercase`, `--lowercase`, `--swapcase`, and `--titlecase` output, and the library API are unchanged (AC5, AC6, FR4).
- No new module, helper, or runtime dependency.

### T002: Add focused CLI unit tests

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- `main(["--casefold", "Straße"])` and `main(["Straße", "--casefold"])` return 0 with stdout `hello, strasse\n` and empty stderr (AC1).
- `"ADA"` → `hello, ada\n` and `"ΣΊΣΥΦΟΣ"` → `hello, σίσυφοσ\n`, each returning 0 (AC2).
- `main(["--casefold", "--prefix", "OK: ", "--quotes", "--repeat", "2", "--no-newline", "Straße"])` returns 0 with stdout `"OK: hello, strasse"\n"OK: hello, strasse"` and empty stderr (AC3).
- `["--casefold", X, "Ada"]` and `[X, "--casefold", "Ada"]` for each X in `--uppercase`, `--lowercase`, `--swapcase`, `--titlecase` raise `SystemExit` with code 2, empty stdout, stderr containing `not allowed with argument` (AC4).
- `--casefold` with each of `""`, `" "`, `"\t"`, `"\n"` raises `SystemExit` code 1, empty stdout, stderr containing `name must not be blank` (AC5).
- `main(["--lowercase", "Straße"])` returns 0 with stdout `hello, straße\n`, and `main(["--help"])` raises `SystemExit` code 0 with stdout containing `--casefold` (AC6).
- `python -m pytest tests/test_cli.py` passes.

### T003: Add pytest-bdd acceptance scenarios

**File(s)**: `tests/features/add_nmg_smoke_casefold_flag.feature`, `tests/features/steps/test_casefold_flag_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- The feature file contains exactly the six scenarios `@SCN001`–`@SCN006` from `specs/197-add-nmg-smoke-casefold-flag/feature.gherkin`, mapped one-to-one to AC1–AC6.
- Steps invoke the installed console script as a subprocess, resolving it with `sysconfig.get_path("scripts")` (`nmg-smoke`, falling back to `nmg-smoke.exe`) as in `tests/features/steps/test_titlecase_steps.py`, with `encoding="utf-8"` and environment `PYTHONIOENCODING=utf-8` so non-ASCII arguments and output are handled identically on every platform.
- The existing `tests/features/steps/test_casefold_steps.py` and `tests/features/add_casefolded_greeting_helper.feature` (library helper, issue #90) are unchanged.
- `python -m pytest tests/features` passes.

### T004: Document --casefold in the README

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- The `## CLI` section, directly after the `--titlecase` documentation, documents `--casefold` with the example `nmg-smoke --casefold Straße` printing `hello, strasse`, states that casefolding uses Python `str.casefold()` and applies before the literal prefix so prefix text keeps its original case, and states that combining `--casefold` with `--uppercase`, `--lowercase`, `--swapcase`, or `--titlecase` is rejected with exit status 2 (FR5).
- Existing CLI and library documentation is otherwise unchanged.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #197 | 2026-10-06 | Initial feature tasks |
