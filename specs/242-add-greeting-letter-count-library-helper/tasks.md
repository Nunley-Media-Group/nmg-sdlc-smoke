# Tasks: Add greeting_letter_count library helper

**Issue**: #242
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/237-add-greeting-unique-char-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_letter_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_letter_count(name: str) -> int` returning `sum(character.isalpha() for character in greet(name))`, immediately after `greeting_unique_char_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_letter_count as greeting_letter_count` and the `__all__` entry `"greeting_letter_count"`, each immediately after its `greeting_length` entry. Remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_letter_count,` after `greeting_length,` in the import list;
  - add `greeting_letter_count("Ada")  # 8` after the `greeting_unique_char_count("Ada")  # 9` example;
  - add the exact `greeting_letter_count` prose line from design.md after the `greeting_unique_char_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_letter_count` to the package-root import list, after `greeting_length`.
- Parameterize `("Ada", 8)`, `("Ada Lovelace", 16)`, `("R2D2", 7)`, `("Zoë", 8)` with precomposed U+00EB, and `("O'Brien", 11)`. For each, assert `type(result) is int` and the exact count (AC1, AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_letter_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_letter_count("Ada") == 8` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_letter_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_letter_count_library_helper.feature`, `tests/features/steps/test_greeting_letter_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_letter_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_unique_char_count_steps.py` (AC1–AC4).
- Assert:
  - results `[8, 16, 7]` for `"Ada"`, `"Ada Lovelace"`, and `"R2D2"`, each of type `int` (AC1);
  - results `[8, 11]` for `"Zoë"` and `"O'Brien"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_letter_count("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "8\n", "")`;
    - `"greeting_letter_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_unique_char_count`) remains;
    - the exact `greeting_letter_count` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_letter_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #242 | 2026-10-24 | Initial feature tasks |
