# Tasks: Add greeting_shortest_word library helper

**Issue**: #338
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_shortest_word

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_shortest_word(name: str) -> str` exactly as in design.md, immediately after `greeting_longest_word` (AC1, AC2, AC3, AC4, AC5, AC6, AC7, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_shortest_word as greeting_shortest_word` immediately after the `greeting_shake_256` import;
  - add the `__all__` entry `"greeting_shortest_word"` immediately after `"greeting_shake_256"`;
  - remove no existing export (AC8, FR3, FR5).
- In README `## Library`:
  - add `greeting_shortest_word,` after `greeting_shake_256,` in the import list;
  - add the `greeting_shortest_word("Ada")  # 'Ada'` example after the `greeting_longest_word("Ada")` example;
  - add the exact `greeting_shortest_word` prose line from design.md after the `greeting_longest_word` prose line (AC8, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_shortest_word_library_helper.feature`, `tests/features/steps/test_greeting_shortest_word_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the eight tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_shortest_word_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_longest_word_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Ada"` for `"Ada"`, `"Ada"` for `"Ada Lovelace"`, and `"007"` for `"Agent 007"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `greeting_shortest_word("Bertha") == "Hello,"` and `greeting_shortest_word("Bo Al") == "Bo"`.
- `@SCN003` (AC3): assert `greeting_shortest_word("Lovelace") == "Hello,"`.
- `@SCN004` (AC4): assert `"Ada"` for `"Ada\tLovelace"`, `"Ada"` for `" Ada "`, and `"Bo"` for `"Bo  Al"`.
- `@SCN005` (AC5): assert `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` for `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`, and `"Hello,"` for `"Chloe\N{COMBINING ACUTE ACCENT}"`.
- `@SCN006` (AC6): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"Bertha"`, `"Bo Al"`, `"O'Brien-Smith"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`, assert:
  - `result in greeting_words(name)`;
  - `len(result) == min(greeting_word_lengths(name))`.
- `@SCN007` (AC7): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN008` (AC8):
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_shortest_word("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Ada\n", "")`;
  - `"greeting_shortest_word" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_longest_word`, `greeting_words`, `greeting_word_lengths`, `greeting_shake_256`, and `greeting_slug`;
  - the exact `greeting_shortest_word` prose line from design.md is one of the lines of `README.md`;
  - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_shortest_word_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #338 | 2026-11-20 | Initial feature tasks |
