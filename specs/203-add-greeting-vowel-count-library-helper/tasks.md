# Tasks: Add greeting_vowel_count library helper

**Issue**: #203
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_vowel_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_vowel_count(name: str) -> int` returning `sum(character in "aeiouAEIOU" for character in greet(name))`, immediately after `greeting_word_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_vowel_count as greeting_vowel_count` and the `__all__` entry `"greeting_vowel_count"`, each immediately after its `greeting_starts_with_hello` entry. Remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_vowel_count,` after `greeting_starts_with_hello,` in the import list;
  - add `greeting_vowel_count("Ada")  # 4` after the `greeting_word_count("Ada Lovelace")  # 3` example;
  - add the exact `greeting_vowel_count` prose line from design.md after the `greeting_word_count` prose line (AC4, FR3).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_vowel_count` to the package-root import list, after `greeting_starts_with_hello`.
- Parameterize these cases. For each, assert `type(result) is int` and the exact count (AC1, AC2):
  - `("Ada", 4)` and `("AEIOU aeiou", 12)`;
  - `("Bcd", 2)` and `("Ady", 3)`;
  - `("\u00c9mile", 4)` and `("\uff21\uff44\uff41", 2)`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_vowel_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_vowel_count("Ada") == 4` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_vowel_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_vowel_count_library_helper.feature`, `tests/features/steps/test_greeting_vowel_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_vowel_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_reversed_steps.py` and `tests/features/steps/test_word_count_steps.py` (AC1–AC4).
- Assert:
  - results `[4, 12]` for `"Ada"` and `"AEIOU aeiou"`, each of type `int` (AC1);
  - results `[2, 3, 4, 2]` for `"Bcd"`, `"Ady"`, `"\u00c9mile"`, and `"\uff21\uff44\uff41"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_vowel_count("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "4\n", "")`;
    - `"greeting_vowel_count" in nmg_sdlc_smoke.__all__`;
    - the exact `greeting_vowel_count` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_vowel_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #203 | 2026-10-18 | Initial feature tasks |
