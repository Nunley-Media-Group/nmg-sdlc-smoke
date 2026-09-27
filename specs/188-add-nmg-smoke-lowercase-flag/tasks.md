# Tasks: Add nmg-smoke --lowercase flag

**Issue**: #188
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/43-add-nmg-smoke-uppercase-flag/

## Implementation Tasks

### T001: Add the mutually exclusive --lowercase flag

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: none
**Acceptance**:
- `--uppercase` and a new long-only boolean `--lowercase` are registered in one `parser.add_mutually_exclusive_group()`; supplying both in either order exits 2 with `not allowed with argument` on stderr and empty stdout (AC4, FR3).
- When `args.lowercase` is true, `message = message.lower()` runs in the `elif` branch after the `args.uppercase` check, before prefix, parentheses, braces, quotes, and the repeat/newline loop (AC1, AC2, AC3, FR1, FR2).
- Blank-name handling, default output, `--uppercase` output, and the library API are unchanged (AC5, AC6, FR4).
- No new module, helper, or runtime dependency.

### T002: Add focused CLI unit tests

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- `main(["--lowercase", "Ada"])` and `main(["Ada", "--lowercase"])` return 0 with stdout `hello, ada\n` and empty stderr (AC1).
- `main(["--lowercase", "--prefix", "OK: ", "--parentheses", "--repeat", "2", "--no-newline", "ADA"])` returns 0 with stdout `(OK: hello, ada)\n(OK: hello, ada)` (AC2).
- `ÅSA` → `hello, åsa\n` and `Straße` → `hello, straße\n` (AC3).
- `["--uppercase", "--lowercase", "Ada"]` and `["--lowercase", "--uppercase", "Ada"]` raise `SystemExit` with code 2, empty stdout, stderr containing `not allowed with argument` (AC4).
- `--lowercase` with each of `""`, `" "`, `"\t"`, `"\n"` raises `SystemExit` code 1, empty stdout, stderr containing `name must not be blank` (AC5).
- `main(["--help"])` raises `SystemExit` code 0 and stdout contains `--lowercase` (AC6).
- `python -m pytest tests/test_cli.py` passes.

### T003: Add pytest-bdd acceptance scenarios

**File(s)**: `tests/features/add_nmg_smoke_lowercase_flag.feature`, `tests/features/steps/test_lowercase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- The feature file contains exactly the six scenarios `@SCN001`–`@SCN006` from `specs/188-add-nmg-smoke-lowercase-flag/feature.gherkin`, mapped one-to-one to AC1–AC6.
- Steps invoke the installed console script as a subprocess, resolving it with `sysconfig.get_path("scripts")` (`nmg-smoke`, falling back to `nmg-smoke.exe`) as in `tests/features/steps/test_quotes_steps.py`, with `encoding="utf-8"` and environment `PYTHONIOENCODING=utf-8` so non-ASCII output is decoded identically on every platform.
- `python -m pytest tests/features` passes.

### T004: Document --lowercase in the README

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- The `## CLI` section, directly after the `--uppercase` example, documents `--lowercase` with the example `nmg-smoke --lowercase Ada` printing `hello, ada`, states that lowercasing applies before the literal prefix, and states that combining `--lowercase` with `--uppercase` is rejected with exit status 2 (FR5).
- Existing CLI and library documentation is otherwise unchanged.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #188 | 2026-09-27 | Initial feature tasks |
