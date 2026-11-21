# Tasks: Add greeting_longest_word library helper

**Issue**: #335
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_longest_word

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_longest_word(name: str) -> str` exactly as in design.md, immediately after `greeting_word_lengths` (AC1, AC2, AC3, AC4, AC5, AC6, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_longest_word as greeting_longest_word` immediately after the `greeting_letter_count` import;
  - add the `__all__` entry `"greeting_longest_word"` immediately after `"greeting_letter_count"`;
  - remove no existing export (AC7, FR3, FR5).
- In README `## Library`:
  - add `greeting_longest_word,` after `greeting_letter_count,` in the import list;
  - add the `greeting_longest_word("Ada")  # 'Hello,'` example after the `greeting_word_lengths("Ada")` example;
  - add the exact `greeting_longest_word` prose line from design.md after the `greeting_word_lengths` prose line (AC7, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_longest_word_library_helper.feature`, `tests/features/steps/test_greeting_longest_word_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the seven tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_longest_word_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_word_lengths_steps.py`. Write non-ASCII inputs as Python escapes.
- `@SCN001` (AC1): assert `"Hello,"` for `"Ada"`, `"Lovelace"` for `"Ada Lovelace"`, and `"Hello,"` for `"Agent 007"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `greeting_longest_word("Bertha") == "Hello,"`.
- `@SCN003` (AC3): assert `"Lovelace"` for `"Ada\tLovelace"`, `"Hello,"` for `" Ada "`, and `"Lovelace"` for `"Ada  Lovelace"`.
- `@SCN004` (AC4): assert `"Hello,"` for `"Chlo\u00e9e"` and `"Chloe\u0301e"` for `"Chloe\u0301e"`.
- `@SCN005` (AC5): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"Bertha"`, `"O'Brien-Smith"`, and `"Chloe\u0301e"`, assert:
  - `result in greeting_words(name)`;
  - `len(result) == max(greeting_word_lengths(name))`.
- `@SCN006` (AC6): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN007` (AC7):
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_longest_word("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Hello,\n", "")`;
  - `"greeting_longest_word" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_word_lengths`, `greeting_words`, `greeting_letter_count`, and `greeting_lowercase_count`;
  - the exact `greeting_longest_word` prose line from design.md is one of the lines of `README.md`;
  - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_longest_word_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #335 | 2026-11-20 | Initial feature tasks |
