# Tasks: Add greeting_last_word library helper

**Issue**: #344
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_last_word

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_last_word(name: str) -> str` exactly as in design.md, immediately after `greeting_average_word_length` (AC1, AC2, AC3, AC4, AC5, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_last_word as greeting_last_word` immediately after the `greeting_is_title` import;
  - add the `__all__` entry `"greeting_last_word"` immediately after `"greeting_is_title"`;
  - remove no existing export (AC6, FR3).
- In README `## Library`:
  - add `greeting_last_word,` after `greeting_is_title,` in the import list;
  - add the `greeting_last_word("Ada Lovelace")  # 'Lovelace'` example after the `greeting_average_word_length("Ada")` example;
  - add the exact `greeting_last_word` prose line from design.md after the `greeting_average_word_length` prose line (AC6, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_last_word_library_helper.feature`, `tests/features/steps/test_greeting_last_word_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the six tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_last_word_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_average_word_length_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Ada"` for `"Ada"`, `"Lovelace"` for `"Ada Lovelace"`, and `"007"` for `"Agent 007"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"Lovelace"` for `"Ada\tLovelace"`, `"Ada"` for `" Ada "`, and `"Al"` for `"Bo  Al\n"`.
- `@SCN003` (AC3): assert `"Ada!"` for `"Ada!"`, `"O'Brien-Smith"` for `"O'Brien-Smith"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"` (length 6) for `"Chloe\N{COMBINING ACUTE ACCENT}"`.
- `@SCN004` (AC4): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"Ada\tLovelace"`, `"O'Brien-Smith"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`, assert `result == greeting_words(name)[-1]`.
- `@SCN005` (AC5): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN006` (AC6):
  - `from nmg_sdlc_smoke import greeting_last_word` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_last_word("Ada Lovelace"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Lovelace\n", "")`;
  - `"greeting_last_word" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_is_title`, `greeting_length`, `greeting_words`, and `greeting_average_word_length`;
  - the exact `greeting_last_word` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_last_word_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #344 | 2026-11-22 | Initial feature tasks |
