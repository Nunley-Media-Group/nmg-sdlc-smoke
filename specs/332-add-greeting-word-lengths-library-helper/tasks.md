# Tasks: Add greeting_word_lengths library helper

**Issue**: #332
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_word_lengths

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_word_lengths(name: str) -> list[int]` exactly as in design.md, immediately after `greeting_words` (AC1, AC2, AC3, AC4, AC5, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_word_lengths as greeting_word_lengths` immediately after the `greeting_word_count` import;
  - add the `__all__` entry `"greeting_word_lengths"` immediately after `"greeting_word_count"`;
  - remove no existing export (AC6, FR3, FR5).
- In README `## Library`:
  - add `greeting_word_lengths,` after `greeting_word_count,` in the import list;
  - add the `greeting_word_lengths("Ada")  # [6, 3]` example after the `greeting_words("Ada")` example;
  - add the exact `greeting_word_lengths` prose line from design.md after the `greeting_words` prose line (AC6, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_word_lengths_library_helper.feature`, `tests/features/steps/test_greeting_word_lengths_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the six tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_word_lengths_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_char_frequency_steps.py`. Write non-ASCII inputs as Python escapes.
- `@SCN001` (AC1): assert `[6, 3]` for `"Ada"`, `[6, 3, 8]` for `"Ada Lovelace"`, and `[6, 5, 3]` for `"Agent 007"`; assert `type(result) is list` and every element `type(v) is int`.
- `@SCN002` (AC2): assert `[6, 3, 3]` for `"Ada\tLee"`, `[6, 3]` for `" Ada "`, and `[6, 3, 3]` for `"Ada  Lee"`; assert `0` is in no result.
- `@SCN003` (AC3): assert `[6, 3]` for `"Zo\u00eb"`, `[6, 4]` for `"Zoe\u0308"`, and `[6, 4]` for `"Ada\U0001F600"`.
- `@SCN004` (AC4): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"O'Brien"`, `"Ada\tLee"`, and `"Zoe\u0308"`, assert:
  - `result == [len(w) for w in greeting_words(name)]`;
  - `len(result) == greeting_word_count(name)`.
- `@SCN005` (AC5): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN006` (AC6):
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_word_lengths("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "[6, 3]\n", "")`;
  - `"greeting_word_lengths" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_word_count`, `greeting_words`, `greeting_initials`, and `greeting_char_frequency`) remains;
  - the exact `greeting_word_lengths` prose line from design.md is one of the lines of `README.md`;
  - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_word_lengths_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #332 | 2026-11-20 | Initial feature tasks |
