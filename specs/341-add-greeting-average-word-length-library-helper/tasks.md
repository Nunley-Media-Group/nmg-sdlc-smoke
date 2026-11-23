# Tasks: Add greeting_average_word_length library helper

**Issue**: #341
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_average_word_length

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_average_word_length(name: str) -> float` exactly as in design.md, immediately after `greeting_shortest_word` (AC1, AC2, AC3, AC4, AC5, AC6, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_average_word_length as greeting_average_word_length` immediately after the `greeting_ascii85` import;
  - add the `__all__` entry `"greeting_average_word_length"` immediately after `"greeting_ascii85"`;
  - remove no existing export (AC7, FR3, FR5).
- In README `## Library`:
  - add `greeting_average_word_length,` after `greeting_ascii85,` in the import list;
  - add the `greeting_average_word_length("Ada")  # 4.5` example after the `greeting_shortest_word("Ada")` example;
  - add the exact `greeting_average_word_length` prose line from design.md after the `greeting_shortest_word` prose line (AC7, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_average_word_length_library_helper.feature`, `tests/features/steps/test_greeting_average_word_length_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the seven tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_average_word_length_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_shortest_word_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `4.5` for `"Ada"`, `17 / 3` for `"Ada Lovelace"`, and `14 / 3` for `"Agent 007"`; assert `type(result) is float` for each.
- `@SCN002` (AC2): assert `greeting_average_word_length("Bertha") == 6.0` and `type(result) is float`.
- `@SCN003` (AC3): assert `17 / 3` for `"Ada\tLovelace"`, `4.5` for `" Ada "`, and `10 / 3` for `"Bo  Al"`.
- `@SCN004` (AC4): assert `5.5` for `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` and `6.0` for `"Chloe\N{COMBINING ACUTE ACCENT}"`.
- `@SCN005` (AC5): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"Bertha"`, `"Bo Al"`, `"O'Brien-Smith"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`, assert:
  - `result == sum(greeting_word_lengths(name)) / len(greeting_words(name))`;
  - `len(greeting_shortest_word(name)) <= result <= len(greeting_longest_word(name))`.
- `@SCN006` (AC6): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN007` (AC7):
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_average_word_length("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "4.5\n", "")`;
  - `"greeting_average_word_length" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_ascii85`, `greeting_base32`, `greeting_words`, `greeting_word_lengths`, `greeting_longest_word`, and `greeting_shortest_word`;
  - the exact `greeting_average_word_length` prose line from design.md is one of the lines of `README.md`;
  - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_average_word_length_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #341 | 2026-11-22 | Initial feature tasks |
