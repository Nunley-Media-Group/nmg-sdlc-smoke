# Tasks: Add greeting_lowercase_count library helper

**Issue**: #224
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/221-add-greeting-uppercase-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_lowercase_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_lowercase_count(name: str) -> int` returning `sum("a" <= character <= "z" for character in greet(name))`, immediately after `greeting_uppercase_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_lowercase_count as greeting_lowercase_count` and the `__all__` entry `"greeting_lowercase_count"`, each immediately after its `greeting_length` entry. Remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_lowercase_count,` after `greeting_length,` in the import list;
  - add `greeting_lowercase_count("Ada")  # 6` after the `greeting_uppercase_count("Ada")  # 2` example;
  - add the exact `greeting_lowercase_count` prose line from design.md after the `greeting_uppercase_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_lowercase_count` to the package-root import list, after `greeting_length`.
- Parameterize these cases. For each, assert `type(result) is int` and the exact count (AC1, AC2):
  - `("Ada", 6)` and `("abc xyz", 10)`;
  - `("BOB 42!", 4)`, `("é", 4)`, and `("ｂｃ", 4)`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_lowercase_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_lowercase_count("Ada") == 6` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_lowercase_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_lowercase_count_library_helper.feature`, `tests/features/steps/test_greeting_lowercase_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_lowercase_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_uppercase_count_steps.py` (AC1–AC4).
- Assert:
  - results `[6, 10]` for `"Ada"` and `"abc xyz"`, each of type `int` (AC1);
  - results `[4, 4, 4]` for `"BOB 42!"`, `"é"`, and `"ｂｃ"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_lowercase_count("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "6\n", "")`;
    - `"greeting_lowercase_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains;
    - the exact `greeting_lowercase_count` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_lowercase_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #224 | 2026-10-24 | Initial feature tasks |
