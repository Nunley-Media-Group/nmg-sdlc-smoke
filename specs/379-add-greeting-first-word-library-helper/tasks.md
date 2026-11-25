# Tasks: Add greeting_first_word library helper

**Issue**: #379
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_first_word

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_first_word(name: str) -> str` exactly as in design.md, immediately before `greeting_last_word` (AC1, AC2, AC3, AC4, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_first_word as greeting_first_word` immediately after the `greeting_ends_with_name` import;
  - add the `__all__` entry `"greeting_first_word"` immediately after `"greeting_ends_with_name"`;
  - remove no existing export (AC5, FR3).
- In README `## Library`:
  - add `greeting_first_word,` after `greeting_ends_with_name,` in the import list;
  - add the `greeting_first_word("Ada Lovelace")  # 'Hello,'` example immediately before the `greeting_last_word("Ada Lovelace")` example;
  - add the exact `greeting_first_word` prose line from design.md immediately before the `greeting_last_word` prose line (AC5, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_first_word_library_helper.feature`, `tests/features/steps/test_greeting_first_word_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_first_word_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_last_word_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Hello,"` for `"Ada"`, `"Ada Lovelace"`, and `"Agent 007"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"Hello,"` (length 6) for `"Ada\tLovelace"`, `" Ada "`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`.
- `@SCN003` (AC3): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"Ada\tLovelace"`, `" Ada "`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`, assert `result == greeting_words(name)[0]`.
- `@SCN004` (AC4): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN005` (AC5):
  - `from nmg_sdlc_smoke import greeting_first_word` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_first_word("Ada Lovelace"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Hello,\n", "")`;
  - `"greeting_first_word" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_ends_with_name`, `greeting_has_apostrophe`, `greeting_last_word`, and `greeting_words`;
  - the exact `greeting_first_word` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_first_word_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #379 | 2026-11-25 | Initial feature tasks |
