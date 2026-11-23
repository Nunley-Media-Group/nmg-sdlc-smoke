# Tasks: Add greeting_capitalize library helper

**Issue**: #365
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_capitalize

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_capitalize(name: str) -> str` exactly as in design.md, immediately after `greeting_titlecase` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_capitalize as greeting_capitalize` immediately after the `greeting_bytes` import;
  - add the `__all__` entry `"greeting_capitalize"` immediately after `"greeting_bytes"`;
  - remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_capitalize,` after `greeting_bytes,` in the import list;
  - add the `greeting_capitalize("Ada Lovelace")  # "Hello, ada lovelace"` example after the `greeting_titlecase("ada lovelace")` example;
  - add the exact `greeting_capitalize` prose line from design.md after the `greeting_titlecase` prose line (AC4, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_capitalize_library_helper.feature`, `tests/features/steps/test_greeting_capitalize_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_capitalize_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_word_frequency_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Hello, ada"` for `"Ada"`, `"Hello, ada lovelace"` for `"Ada Lovelace"`, `"Hello, ada"` for `"ADA"`, and `"Hello, ada lovelace"` for `"ada lovelace"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"Hello, o'brien-smith"` for `"O'BRIEN-SMITH"`, `"Hello, ada 42"` for `"Ada 42"`, `"Hello, \N{LATIN SMALL LETTER E WITH ACUTE}mile"` for `"\N{LATIN CAPITAL LETTER E WITH ACUTE}MILE"`, and `"Hello,  ada "` for `" Ada "`; for each, assert the result equals `greet(name).capitalize()`.
- `@SCN003` (AC3): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN004` (AC4):
  - `from nmg_sdlc_smoke import greeting_capitalize` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_capitalize("Ada Lovelace"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Hello, ada lovelace\n", "")`;
  - `"greeting_capitalize" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_bytes`, `greeting_casefold`, `greeting_swapcase`, `greeting_titlecase`, and `greeting_word_frequency`;
  - the exact `greeting_capitalize` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_capitalize_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #365 | 2026-11-23 | Initial feature tasks |
