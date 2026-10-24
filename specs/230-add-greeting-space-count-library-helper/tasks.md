# Tasks: Add greeting_space_count library helper

**Issue**: #230
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/227-add-greeting-digit-count-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_space_count

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_space_count(name: str) -> int` returning `greet(name).count(" ")`, immediately after `greeting_digit_count` (AC1, AC2, AC3, FR1, FR2, FR3).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_space_count as greeting_space_count` and the `__all__` entry `"greeting_space_count"`, each immediately after its `greeting_sha256` entry. Remove no existing export (AC4, FR4, FR5).
- In README `## Library`:
  - add `greeting_space_count,` after `greeting_sha256,` in the import list;
  - add `greeting_space_count("Ada Lovelace")  # 2` after the `greeting_digit_count("R2D2")  # 2` example;
  - add the exact `greeting_space_count` prose line from design.md after the `greeting_digit_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_space_count` to the package-root import list, after `greeting_sha256`.
- Parameterize these cases. For each, assert `type(result) is int` and the exact count (AC1, AC2):
  - `("Ada", 1)`, `("Ada Lovelace", 2)`, and `("Grace Brewster Hopper", 3)`;
  - `("Ada\tLovelace", 1)`, `("Ada\nLovelace", 1)`, and `("Ada\u00a0Lovelace", 1)`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_space_count" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_space_count("Ada Lovelace") == 2` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_space_count`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_space_count_library_helper.feature`, `tests/features/steps/test_greeting_space_count_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_space_count_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_digit_count_steps.py` (AC1–AC4).
- Assert:
  - results `[1, 2, 3]` for `"Ada"`, `"Ada Lovelace"`, and `"Grace Brewster Hopper"`, each of type `int` (AC1);
  - results `[1, 1, 1]` for `"Ada\tLovelace"`, `"Ada\nLovelace"`, and `"Ada\u00a0Lovelace"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_space_count("Ada Lovelace"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "2\n", "")`;
    - `"greeting_space_count" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains;
    - the exact `greeting_space_count` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_space_count_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #230 | 2026-10-24 | Initial feature tasks |
