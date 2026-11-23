# Tasks: Add greeting_word_frequency library helper

**Issue**: #362
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_word_frequency

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_word_frequency(name: str) -> dict[str, int]` exactly as in design.md, immediately after `greeting_last_word` (AC1, AC2, AC3, AC4, AC5, AC6, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_word_frequency as greeting_word_frequency` immediately after the `greeting_word_count` import;
  - add the `__all__` entry `"greeting_word_frequency"` immediately after `"greeting_word_count"`;
  - remove no existing export (AC7, FR3).
- In README `## Library`:
  - add `greeting_word_frequency,` after `greeting_word_count,` in the import list;
  - add the `greeting_word_frequency("Bo Bo")  # {"Hello,": 1, "Bo": 2}` example after the `greeting_last_word("Ada Lovelace")` example;
  - add the exact `greeting_word_frequency` prose line from design.md after the `greeting_last_word` prose line (AC7, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_word_frequency_library_helper.feature`, `tests/features/steps/test_greeting_word_frequency_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the seven tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_word_frequency_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_char_frequency_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1):
  - assert `{"Hello,": 1, "Ada": 1}` for `"Ada"`, `{"Hello,": 1, "Ada": 1, "Lovelace": 1}` for `"Ada Lovelace"`, and `{"Hello,": 1, "Bo": 2}` for `"Bo Bo"`;
  - assert `list(result)` equals the expected key order and `type(result) is dict` for each.
- `@SCN002` (AC2): assert `{"Hello,": 1, "Bo": 2}` for `"Bo\tBo"`, `{"Hello,": 1, "Ada": 1}` for `" Ada "`, and `{"Hello,": 1, "Bo": 2, "Al": 1}` for `"Bo  Al\nBo"`, including key order.
- `@SCN003` (AC3): assert `{"Hello,": 1, "Bo": 1, "bo": 1}` for `"Bo bo"`, `{"Hello,": 2, "Hello": 1}` for `"Hello Hello,"`, and `{"Hello,": 1, "Chloe\N{COMBINING ACUTE ACCENT}": 1, "Chlo\N{LATIN SMALL LETTER E WITH ACUTE}": 1}` for `"Chloe\N{COMBINING ACUTE ACCENT} Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`.
- `@SCN004` (AC4): for `"Ada"`, `"Bo Bo"`, `"Bo  Al\nBo"`, `"O'Brien-Smith"`, and `"Hello Hello,"`, assert `sum(result.values()) == greeting_word_count(name)` and `list(result) == list(dict.fromkeys(greeting_words(name)))`.
- `@SCN005` (AC5): call `greeting_word_frequency("Ada")` twice and mutate the first result (set `"Ada"` to `99` and add key `"x"`); assert the second result is `{"Hello,": 1, "Ada": 1}` and is not the same object as the first.
- `@SCN006` (AC6): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN007` (AC7):
  - `from nmg_sdlc_smoke import greeting_word_frequency` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_word_frequency("Bo Bo"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "{'Hello,': 1, 'Bo': 2}\n", "")`;
  - `"greeting_word_frequency" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_char_frequency`, `greeting_word_count`, `greeting_word_lengths`, `greeting_words`, and `greeting_last_word`;
  - the exact `greeting_word_frequency` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_word_frequency_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #362 | 2026-11-23 | Initial feature tasks |
