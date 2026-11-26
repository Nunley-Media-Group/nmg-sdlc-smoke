# Tasks: Add greeting_ascii_count library helper

**Issue**: #383
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_ascii_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_ascii_count(name: str) -> int` exactly as in design.md, immediately after `greeting_non_ascii_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_ascii_count as greeting_ascii_count` immediately after the `greeting_ascii85` import;
  - add the `__all__` entry `"greeting_ascii_count"` immediately after `"greeting_ascii85"`;
  - remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_ascii_count,` after `greeting_ascii85,` in the import list;
  - add the `greeting_ascii_count("Zo\u00eb")  # 9` example after the `greeting_non_ascii_count("Zo\u00eb")  # 1` example;
  - add the exact `greeting_ascii_count` prose line from design.md after the `greeting_non_ascii_count` prose line (AC4, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_ascii_count_library_helper.feature`, `tests/features/steps/test_greeting_ascii_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_ascii_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_non_ascii_count_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `10` for `"Ada"`, `9` for `"Zo\N{LATIN SMALL LETTER E WITH DIAERESIS}"`, and `7` for `"\N{CJK UNIFIED IDEOGRAPH-674E}\N{CJK UNIFIED IDEOGRAPH-96F7}"`; assert `type(result) is int` for each.
- `@SCN002` (AC2):
  - assert `10` for `"Zoe\N{COMBINING DIAERESIS}"` and `11` for `"Ada \N{GRINNING FACE}"`;
  - for each name in AC1 and AC2, assert the result equals `sum(ord(ch) <= 127 for ch in greet(name))`;
  - for each name in AC1 and AC2, assert `greeting_ascii_count(name) + greeting_non_ascii_count(name) == len(greet(name))`.
- `@SCN003` (AC3): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN004` (AC4):
  - `from nmg_sdlc_smoke import greeting_ascii_count` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_ascii_count("Zo\u00eb"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "9\n", "")`;
  - `"greeting_ascii_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_ascii85`, `greeting_average_word_length`, `greeting_is_ascii`, and `greeting_non_ascii_count`;
  - the exact `greeting_ascii_count` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_ascii_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #383 | 2026-11-25 | Initial feature tasks |
