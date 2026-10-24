# Tasks: Add greeting_consonant_count library helper

**Issue**: #213
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/203-add-greeting-vowel-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_consonant_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_consonant_count(name: str) -> int` immediately after `greeting_vowel_count`. It returns `sum(character in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ" for character in greet(name))` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_consonant_count as greeting_consonant_count` and the `__all__` entry `"greeting_consonant_count"`, each immediately after its `greeting_casefold` entry. Remove no existing export (AC4, FR3).
- In README `## Library` (AC4, FR3):
  - add `greeting_consonant_count,` after `greeting_casefold,` in the import list;
  - add `greeting_consonant_count("Ada")  # 4` after the `greeting_vowel_count("Ada")  # 4` example;
  - add the exact `greeting_consonant_count` prose line from design.md after the `greeting_vowel_count` prose line.
- `nmg-smoke` CLI source is unchanged.

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_consonant_count` to the package-root import list, after `greeting_casefold`.
- Parameterize these cases. For each, assert `type(result) is int` and the exact count (AC1, AC2):
  - `("Ada", 4)` and `("BCDFGHJKLMNPQRSTVWXYZ bcdfghjklmnpqrstvwxyz", 45)`;
  - `("Ady", 5)`, `("Yy", 5)`, and `("Bob 42!", 5)`;
  - `("Émile", 5)` and `("Ｂｃｄ", 3)`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_consonant_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_consonant_count("Ada") == 4` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_consonant_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_consonant_count_library_helper.feature`, `tests/features/steps/test_greeting_consonant_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_consonant_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_vowel_count_steps.py` and `tests/features/steps/test_greeting_base64_steps.py` (AC1–AC4).
- Assert:
  - results `[4, 45]` for `"Ada"` and the all-consonants name, each of type `int` (AC1);
  - results `[5, 5, 5, 5, 3]` for `"Ady"`, `"Yy"`, `"Bob 42!"`, `"Émile"`, and `"Ｂｃｄ"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_consonant_count("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "4\n", "")`;
    - `"greeting_consonant_count" in nmg_sdlc_smoke.__all__`;
    - the installed `nmg-smoke` script is located through `sysconfig.get_path("scripts")`, with a `.exe` fallback, and running it with `Ada` gives `(0, "Hello, Ada\n", "")`;
    - the exact `greeting_consonant_count` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_consonant_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #213 | 2026-10-24 | Initial feature tasks |
