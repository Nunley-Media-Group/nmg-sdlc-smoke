# Tasks: Add greeting_digit_count library helper

**Issue**: #227
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/224-add-greeting-lowercase-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_digit_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_digit_count(name: str) -> int` returning `sum("0" <= character <= "9" for character in greet(name))`, immediately after `greeting_lowercase_count` (AC1, AC2, AC3, FR1, FR2, FR3).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_digit_count as greeting_digit_count` and the `__all__` entry `"greeting_digit_count"`, each immediately after its `greeting_casefold` entry. Remove no existing export (AC4, FR4, FR5).
- In README `## Library`:
  - add `greeting_digit_count,` after `greeting_casefold,` in the import list;
  - add `greeting_digit_count("R2D2")  # 2` after the `greeting_lowercase_count("Ada")  # 6` example;
  - add the exact `greeting_digit_count` prose line from design.md after the `greeting_lowercase_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_digit_count` to the package-root import list, after `greeting_casefold`.
- Parameterize these cases. For each, assert `type(result) is int` and the exact count (AC1, AC2):
  - `("R2D2", 2)`, `("Agent 007", 3)`, and `("Ada", 0)`;
  - `("１２", 0)`, `("٣", 0)`, and `("x²", 0)`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_digit_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_digit_count("R2D2") == 2` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_digit_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_digit_count_library_helper.feature`, `tests/features/steps/test_greeting_digit_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_digit_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_lowercase_count_steps.py` (AC1–AC4).
- Assert:
  - results `[2, 3, 0]` for `"R2D2"`, `"Agent 007"`, and `"Ada"`, each of type `int` (AC1);
  - results `[0, 0, 0]` for `"１２"`, `"٣"`, and `"x²"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_digit_count("R2D2"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "2\n", "")`;
    - `"greeting_digit_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains;
    - the exact `greeting_digit_count` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_digit_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #227 | 2026-10-24 | Initial feature tasks |
