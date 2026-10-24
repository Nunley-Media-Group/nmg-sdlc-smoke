# Tasks: Add greeting_unique_char_count library helper

**Issue**: #237
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/233-add-greeting-punctuation-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_unique_char_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_unique_char_count(name: str) -> int` returning `len(set(greet(name)))`, immediately after `greeting_punctuation_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_unique_char_count as greeting_unique_char_count` and the `__all__` entry `"greeting_unique_char_count"`, each immediately after its `greeting_starts_with_hello` entry. Remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_unique_char_count,` after `greeting_starts_with_hello,` in the import list;
  - add `greeting_unique_char_count("Ada")  # 9` after the `greeting_punctuation_count("O'Brien")  # 2` example;
  - add the exact `greeting_unique_char_count` prose line from design.md after the `greeting_punctuation_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_unique_char_count` to the package-root import list, after `greeting_starts_with_hello`.
- Parameterize `("Ada", 9)`, `("Bob", 8)`, `("Ada Lovelace", 12)`, `("ADA", 8)`, and `("Zoë", 8)` with precomposed U+00EB. For each, assert `type(result) is int` and the exact count (AC1, AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_unique_char_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_unique_char_count("Ada") == 9` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_unique_char_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_unique_char_count_library_helper.feature`, `tests/features/steps/test_greeting_unique_char_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_unique_char_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_punctuation_count_steps.py` (AC1–AC4).
- Assert:
  - results `[9, 8, 12]` for `"Ada"`, `"Bob"`, and `"Ada Lovelace"`, each of type `int` (AC1);
  - results `[8, 8]` for `"ADA"` and `"Zoë"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_unique_char_count("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "9\n", "")`;
    - `"greeting_unique_char_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_punctuation_count`) remains;
    - the exact `greeting_unique_char_count` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_unique_char_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #237 | 2026-10-24 | Initial feature tasks |
