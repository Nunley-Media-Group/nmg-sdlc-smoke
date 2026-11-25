# Tasks: Add greeting_uppercase library helper

**Issue**: #371
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_uppercase

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_uppercase(name: str) -> str` exactly as in design.md, immediately after `greeting_capitalize` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_uppercase as greeting_uppercase` immediately after the `greeting_unique_char_count` import;
  - add the `__all__` entry `"greeting_uppercase"` immediately after `"greeting_unique_char_count"`;
  - remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_uppercase,` after `greeting_unique_char_count,` in the import list;
  - add the `greeting_uppercase("Ada")  # "HELLO, ADA"` example after the `greeting_capitalize("Ada Lovelace")` example;
  - add the exact `greeting_uppercase` prose line from design.md after the `greeting_capitalize` prose line (AC4, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_uppercase_library_helper.feature`, `tests/features/steps/test_greeting_uppercase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_uppercase_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_capitalize_steps.py`. Write non-ASCII inputs and expectations as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"HELLO, ADA"` for `"Ada"`, `"HELLO, ADA LOVELACE"` for `"ada lovelace"`, and `"HELLO, AGENT 007"` for `"Agent 007"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"HELLO, STRASSE"` for `"stra\N{LATIN SMALL LETTER SHARP S}e"`, `"HELLO, \N{LATIN CAPITAL LETTER E WITH ACUTE}MILE"` for `"\N{LATIN SMALL LETTER E WITH ACUTE}mile"`, and `"HELLO, ADA\tBO"` for `"Ada\tBo"`; for each, assert the result equals `greet(name).upper()`.
- `@SCN003` (AC3): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN004` (AC4):
  - `from nmg_sdlc_smoke import greeting_uppercase` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_uppercase("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "HELLO, ADA\n", "")`;
  - `"greeting_uppercase" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_capitalize`, `greeting_unique_char_count`, `greeting_uppercase_count`, `greeting_titlecase`, and `greeting_json`;
  - the exact `greeting_uppercase` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_uppercase_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #371 | 2026-11-25 | Initial feature tasks |
