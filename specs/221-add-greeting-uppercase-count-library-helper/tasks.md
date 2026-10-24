# Tasks: Add greeting_uppercase_count library helper

**Issue**: #221
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/203-add-greeting-vowel-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_uppercase_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_uppercase_count(name: str) -> int` returning `sum("A" <= character <= "Z" for character in greet(name))`, immediately after `greeting_vowel_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_uppercase_count as greeting_uppercase_count` and the `__all__` entry `"greeting_uppercase_count"`, each immediately after its `greeting_starts_with_hello` entry. Remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_uppercase_count,` after `greeting_starts_with_hello,` in the import list;
  - add `greeting_uppercase_count("Ada")  # 2` after the `greeting_vowel_count("Ada")  # 4` example;
  - add the exact `greeting_uppercase_count` prose line from design.md after the `greeting_vowel_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_uppercase_count` to the package-root import list, after `greeting_starts_with_hello`.
- Parameterize these cases. For each, assert `type(result) is int` and the exact count (AC1, AC2):
  - `("Ada", 2)` and `("ABC XYZ", 7)`;
  - `("bob 42!", 1)`, `("Émile", 1)`, and `("ＢＣ", 1)`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_uppercase_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_uppercase_count("Ada") == 2` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_uppercase_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_uppercase_count_library_helper.feature`, `tests/features/steps/test_greeting_uppercase_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_uppercase_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_vowel_count_steps.py` (AC1–AC4).
- Assert:
  - results `[2, 7]` for `"Ada"` and `"ABC XYZ"`, each of type `int` (AC1);
  - results `[1, 1, 1]` for `"bob 42!"`, `"Émile"`, and `"ＢＣ"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_uppercase_count("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "2\n", "")`;
    - `"greeting_uppercase_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains;
    - the exact `greeting_uppercase_count` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_uppercase_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #221 | 2026-10-24 | Initial feature tasks |
