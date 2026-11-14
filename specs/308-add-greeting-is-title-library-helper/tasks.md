# Tasks: Add greeting_is_title library helper

**Issue**: #308
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/305-add-greeting-is-printable-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_is_title

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_is_title(name: str) -> bool` returning `greet(name).istitle()` immediately after `greeting_is_printable` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_is_title as greeting_is_title` immediately after the `greeting_is_printable` import;
  - add the `__all__` entry `"greeting_is_title"` immediately after `"greeting_is_printable"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_is_title,` after `greeting_is_printable,` in the import list;
  - add the `greeting_is_title("Ada")  # True` and `greeting_is_title("ada")  # False` examples after the `greeting_is_printable("Ada\tLovelace")  # False` example;
  - add the exact `greeting_is_title` prose line from design.md after the `greeting_is_printable` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_is_title` to the package-root import list after `greeting_is_printable`.
- Parameterize `"Ada"`, `"Zoë"`, `"Ada Lovelace"`, and `"O'Neil"`. For each, assert that the result `is True` and equals `greet(name).istitle()` (AC1).
- Parameterize `"ada"`, `"ADA"`, `"Ada lovelace"`, and `"McAdam"`. For each, assert that the result `is False` and equals `greet(name).istitle()` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_is_title" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_is_title("Ada") is True` (AC4).
- If existing `__all__` snapshot tests in `tests/test_greet.py` enumerate the full export list, add `"greeting_is_title"` after `"greeting_is_printable"` there.
- Run `python -m pytest tests/test_greet.py -k greeting_is_title`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_is_title_library_helper.feature`, `tests/features/steps/test_greeting_is_title_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_is_title_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_is_printable_steps.py` (AC1–AC4).
- Assert:
  - `True`, as a `bool` equal to `greet(name).istitle()`, for `"Ada"`, `"Zoë"`, `"Ada Lovelace"`, and `"O'Neil"` (AC1);
  - `False`, as a `bool` equal to `greet(name).istitle()`, for `"ada"`, `"ADA"`, `"Ada lovelace"`, and `"McAdam"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_is_title("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "True\n", "")`;
    - `"greeting_is_title" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_is_printable` and `greeting_length`) remains;
    - the exact `greeting_is_title` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_is_title_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #308 | 2026-11-14 | Initial feature tasks |
