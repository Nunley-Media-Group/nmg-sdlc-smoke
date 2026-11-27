# Tasks: Add greeting_alnum_count library helper

**Issue**: #386
**Date**: 2026-11-27
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_alnum_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_alnum_count(name: str) -> int` exactly as in design.md, immediately after `greeting_letter_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_alnum_count as greeting_alnum_count` immediately after the `greeting_adler32` import;
  - add the `__all__` entry `"greeting_alnum_count"` immediately after `"greeting_adler32"`;
  - remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_alnum_count,` after `greeting_adler32,` in the import list;
  - add the `greeting_alnum_count("R2-D2")  # 9` example after the `greeting_letter_count("Ada")  # 8` example;
  - add the exact `greeting_alnum_count` prose line from design.md after the `greeting_letter_count` prose line (AC4, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_alnum_count_library_helper.feature`, `tests/features/steps/test_greeting_alnum_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_alnum_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_ascii_count_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `8` for `"Ada"`, `8` for `"Zo\N{LATIN SMALL LETTER E WITH DIAERESIS}"`, `7` for `"\N{CJK UNIFIED IDEOGRAPH-674E}\N{CJK UNIFIED IDEOGRAPH-96F7}"`, and `9` for `"R2-D2"`; assert `type(result) is int` for each.
- `@SCN002` (AC2):
  - assert `8` for `"Zoe\N{COMBINING DIAERESIS}"`, `8` for `"Ada \N{GRINNING FACE}"`, and `11` for `"Agent \N{ARABIC-INDIC DIGIT THREE}"`;
  - for each name in AC1 and AC2, assert the result equals `sum(ch.isalnum() for ch in greet(name))`.
- `@SCN003` (AC3): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN004` (AC4):
  - `from nmg_sdlc_smoke import greeting_alnum_count` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_alnum_count("R2-D2"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "9\n", "")`;
  - `"greeting_alnum_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_adler32`, `greeting_ascii85`, `greeting_letter_count`, and `greeting_digit_count`;
  - the exact `greeting_alnum_count` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_alnum_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #386 | 2026-11-27 | Initial feature tasks |
