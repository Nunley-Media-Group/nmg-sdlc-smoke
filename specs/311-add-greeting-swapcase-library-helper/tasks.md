# Tasks: Add greeting_swapcase library helper

**Issue**: #311
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/308-add-greeting-is-title-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_swapcase

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_swapcase(name: str) -> str` returning `greet(name).swapcase()` immediately after `greeting_casefold` (AC1, AC2, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_swapcase as greeting_swapcase` immediately after the `greeting_starts_with_hello` import;
  - add the `__all__` entry `"greeting_swapcase"` immediately after `"greeting_starts_with_hello"`;
  - remove no existing export (AC3, FR3, FR5).
- In README `## Library`:
  - add `greeting_swapcase,` after `greeting_starts_with_hello,` in the import list;
  - add the `greeting_swapcase("Ada")  # "hELLO, aDA"` example after the `greeting_casefold("Straße")  # "hello, strasse"` example;
  - add the exact `greeting_swapcase` prose line from design.md after the `greeting_casefold` prose line (AC3, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_swapcase` to the package-root import list after `greeting_starts_with_hello`.
- Parameterize `("Ada", "hELLO, aDA")`, `("Zoë", "hELLO, zOË")`, and `("O'Neil 42", "hELLO, o'nEIL 42")`. For each, assert the result is a `str`, equals the expected value, and equals `greet(name).swapcase()` (AC1).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC2).
- Assert `"greeting_swapcase" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_swapcase("Ada") == "hELLO, aDA"` (AC3).
- If existing `__all__` snapshot tests in `tests/test_greet.py` enumerate the full export list, add `"greeting_swapcase"` after `"greeting_starts_with_hello"` there.
- Run `python -m pytest tests/test_greet.py -k greeting_swapcase`.

### T003: Exercise three AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_swapcase_library_helper.feature`, `tests/features/steps/test_greeting_swapcase_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the three tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_swapcase_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_is_title_steps.py` (AC1–AC3).
- Assert:
  - `"hELLO, aDA"`, `"hELLO, zOË"`, and `"hELLO, o'nEIL 42"` for `"Ada"`, `"Zoë"`, and `"O'Neil 42"`, each a `str` equal to `greet(name).swapcase()` (AC1);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC2);
  - the README example and unchanged CLI (AC3), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_swapcase("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "hELLO, aDA\n", "")`;
    - `"greeting_swapcase" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_starts_with_hello` and `greeting_casefold`) remains;
    - the exact `greeting_swapcase` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_swapcase_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #311 | 2026-11-14 | Initial feature tasks |
