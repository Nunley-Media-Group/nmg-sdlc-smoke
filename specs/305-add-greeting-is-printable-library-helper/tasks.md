# Tasks: Add greeting_is_printable library helper

**Issue**: #305
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/57-add-greeting-is-ascii-library-function/

## Implementation Tasks

### T001: Implement, export, and document greeting_is_printable

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_is_printable(name: str) -> bool` returning `greet(name).isprintable()` immediately after `greeting_is_ascii` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_is_printable as greeting_is_printable` immediately after the `greeting_is_ascii` import;
  - add the `__all__` entry `"greeting_is_printable"` immediately after `"greeting_is_ascii"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_is_printable,` after `greeting_is_ascii,` in the import list;
  - add the `greeting_is_printable("Ada")  # True` and `greeting_is_printable("Ada\tLovelace")  # False` examples after the `greeting_is_ascii("Ada")  # True` example;
  - add the exact `greeting_is_printable` prose line from design.md after the `greet` rejection prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_is_printable` to the package-root import list after `greeting_is_ascii`.
- Parameterize `"Ada"`, `"Zoë"`, and `"Ada Lovelace"`. For each, assert that the result `is True` and equals `greet(name).isprintable()` (AC1).
- Parameterize `"Ada\tLovelace"` and `"Ada\n"`. For each, assert that the result `is False` and equals `greet(name).isprintable()` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_is_printable" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_is_printable("Ada") is True` (AC4).
- If existing `__all__` snapshot tests in `tests/test_greet.py` enumerate the full export list, add `"greeting_is_printable"` after `"greeting_is_ascii"` there.
- Run `python -m pytest tests/test_greet.py -k greeting_is_printable`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_is_printable_library_helper.feature`, `tests/features/steps/test_greeting_is_printable_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_is_printable_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_html_escaped_steps.py` (AC1–AC4).
- Assert:
  - `True`, as a `bool` equal to `greet(name).isprintable()`, for `"Ada"`, `"Zoë"`, and `"Ada Lovelace"` (AC1);
  - `False`, as a `bool` equal to `greet(name).isprintable()`, for `"Ada\tLovelace"` and `"Ada\n"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_is_printable("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "True\n", "")`;
    - `"greeting_is_printable" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_is_ascii` and `greeting_length`) remains;
    - the exact `greeting_is_printable` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_is_printable_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #305 | 2026-11-14 | Initial feature tasks |
