# Tasks: Add greeting_char_frequency library helper

**Issue**: #329
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_char_frequency

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_char_frequency(name: str) -> dict[str, int]` exactly as in design.md, immediately after `greeting_unique_char_count` (AC1, AC2, AC3, AC4, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_char_frequency as greeting_char_frequency` immediately after the `greeting_casefold` import;
  - add the `__all__` entry `"greeting_char_frequency"` immediately after `"greeting_casefold"`;
  - remove no existing export (AC5, FR3, FR5).
- In README `## Library`:
  - add `greeting_char_frequency,` after `greeting_casefold,` in the import list;
  - add the `greeting_char_frequency("Ada")` example from design.md after the `greeting_codepoints("Ada")` example;
  - add the exact `greeting_char_frequency` prose line from design.md after the `greeting_codepoints` prose line (AC5, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_char_frequency_library_helper.feature`, `tests/features/steps/test_greeting_char_frequency_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_char_frequency_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_slug_steps.py`. Write non-ASCII inputs as Python escapes.
- `@SCN001` (AC1): assert the exact AC1 dicts for `"Ada"` and `"Ada Lovelace"`, and assert that `list(result)` equals the AC1 key order and `type(result) is dict`.
- `@SCN002` (AC2):
  - for `"Zo\u00eb"`, assert `"\u00eb": 1` and `"e": 1`;
  - for `"Zoe\u0308"`, assert `"e": 2` and `"\u0308": 1`, with no `"\u00eb"` key;
  - in both, assert `"H": 1` and no `"h"` key.
- `@SCN003` (AC3): for `"Ada"`, `"Ada Lovelace"`, `"Agent 007"`, `"O'Brien"`, `"Zo\u00eb"`, and `"Ada\u674eLee"`, assert:
  - `sum(values) == greeting_length(name)`;
  - `len(result) == greeting_unique_char_count(name)`;
  - every value is a positive `int`.
- `@SCN004` (AC4): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN005` (AC5):
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_char_frequency("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, repr(<AC1 Ada dict>) + "\n", "")`;
  - `"greeting_char_frequency" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_casefold`, `greeting_codepoints`, `greeting_slug`, and `greeting_unique_char_count`) remains;
  - the exact `greeting_char_frequency` prose line from design.md is one of the lines of `README.md`;
  - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_char_frequency_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #329 | 2026-11-19 | Initial feature tasks |
