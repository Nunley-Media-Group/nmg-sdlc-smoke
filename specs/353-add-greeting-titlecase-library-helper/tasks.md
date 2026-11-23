# Tasks: Add greeting_titlecase library helper

**Issue**: #353
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_titlecase

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_titlecase(name: str) -> str` exactly as in design.md, immediately after `greeting_swapcase` (AC1, AC2, AC3, AC4, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_titlecase as greeting_titlecase` immediately after the `greeting_swapcase` import;
  - add the `__all__` entry `"greeting_titlecase"` immediately after `"greeting_swapcase"`;
  - remove no existing export (AC5, FR3).
- In README `## Library`:
  - add `greeting_titlecase,` after `greeting_swapcase,` in the import list;
  - add the `greeting_titlecase("ada lovelace")  # "Hello, Ada Lovelace"` example after the `greeting_swapcase("Ada")` example;
  - add the exact `greeting_titlecase` prose line from design.md after the `greeting_swapcase` prose line (AC5, FR4).
- `src/nmg_sdlc_smoke/cli.py` is unchanged.
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_titlecase_library_helper.feature`, `tests/features/steps/test_greeting_titlecase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_titlecase_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_last_word_steps.py` for library steps and `tests/features/steps/test_casefold_flag_steps.py` for locating and running the installed `nmg-smoke` console script. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Hello, Ada"` for `"ada"`, `"Hello, Ada Lovelace"` for `"ADA LOVELACE"`, and `"Hello, Ada Lovelace"` for `"ada lovelace"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"Hello, O'Brien"` for `"o'brien"`, `"Hello, Agent 007X"` for `"agent 007x"`, and `"Hello, \N{LATIN CAPITAL LETTER A WITH RING ABOVE}sa"` for `"\N{LATIN SMALL LETTER A WITH RING ABOVE}sa"`.
- `@SCN003` (AC3): for `"ada"`, `"ADA LOVELACE"`, `"o'brien"`, and `"Ada\tLovelace"`, assert `result == greet(name).title()`; run the installed `nmg-smoke --titlecase ada` with `encoding="utf-8"` and `PYTHONIOENCODING=utf-8`, and assert `(returncode, stdout, stderr) == (0, greeting_titlecase("ada") + "\n", "")`.
- `@SCN004` (AC4): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN005` (AC5):
  - `from nmg_sdlc_smoke import greeting_titlecase` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_titlecase("ada lovelace"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Hello, Ada Lovelace\n", "")`;
  - `"greeting_titlecase" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_swapcase`, `greeting_is_title`, `greeting_casefold`, and `greeting_last_word`;
  - the exact `greeting_titlecase` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_titlecase_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #353 | 2026-11-23 | Initial feature tasks |
