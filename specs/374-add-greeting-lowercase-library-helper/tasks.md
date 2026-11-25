# Tasks: Add greeting_lowercase library helper

**Issue**: #374
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_lowercase

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_lowercase(name: str) -> str` exactly as in design.md, immediately after `greeting_uppercase` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_lowercase as greeting_lowercase` immediately after the `greeting_longest_word` import;
  - add the `__all__` entry `"greeting_lowercase"` immediately after `"greeting_longest_word"`;
  - remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_lowercase,` after `greeting_longest_word,` in the import list;
  - add the `greeting_lowercase("Ada")  # "hello, ada"` example after the `greeting_uppercase("Ada")` example;
  - add the exact `greeting_lowercase` prose line from design.md after the `greeting_uppercase` prose line (AC4, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_lowercase_library_helper.feature`, `tests/features/steps/test_greeting_lowercase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_lowercase_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_uppercase_steps.py`. Write non-ASCII inputs and expectations as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"hello, ada"` for `"Ada"`, `"hello, ada lovelace"` for `"ADA LOVELACE"`, and `"hello, agent 007"` for `"Agent 007"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"hello, stra\N{LATIN SMALL LETTER SHARP S}e"` for `"Stra\N{LATIN SMALL LETTER SHARP S}e"`, `"hello, \N{LATIN SMALL LETTER E WITH ACUTE}mile"` for `"\N{LATIN CAPITAL LETTER E WITH ACUTE}MILE"`, and `"hello, ada\tbo"` for `"Ada\tBo"`; for each, assert the result equals `greet(name).lower()`.
- `@SCN003` (AC3): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN004` (AC4):
  - `from nmg_sdlc_smoke import greeting_lowercase` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_lowercase("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "hello, ada\n", "")`;
  - `"greeting_lowercase" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_uppercase`, `greeting_casefold`, `greeting_longest_word`, `greeting_lowercase_count`, and `greeting_json`;
  - the exact `greeting_lowercase` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_lowercase_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #374 | 2026-11-25 | Initial feature tasks |
