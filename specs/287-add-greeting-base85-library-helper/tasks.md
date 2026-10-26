# Tasks: Add greeting_base85 library helper

**Issue**: #287
**Date**: 2026-10-26
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/263-add-greeting-base32-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_base85

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_base85(name: str) -> str` returning `base64.b85encode(greet(name).encode("utf-8")).decode("ascii")`, immediately after `greeting_base64`, using the existing `base64` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_base85 as greeting_base85` immediately after the `greeting_base64` import;
  - add the `__all__` entry `"greeting_base85"` immediately after `"greeting_base64"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_base85,` after `greeting_base64,` in the import list;
  - add the `greeting_base85("Ada")  # "NM&qnZ!91|WMK"` example after the `greeting_base32("Ada")` example;
  - add the exact `greeting_base85` prose line from design.md after the `greeting_base32` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_base85` to the package-root import list after `greeting_base64`. The module already imports `base64`.
- Parameterize `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` (precomposed U+00EB) with their exact results from AC1 and AC2. For each, assert `type(result) is str` and the exact value (AC1, AC2).
- Assert `greeting_base85("Zoë") == base64.b85encode("Hello, Zoë".encode("utf-8")).decode("ascii")` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_base85" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_base85("Ada") == "NM&qnZ!91|WMK"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_base85`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_base85_library_helper.feature`, `tests/features/steps/test_greeting_base85_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_base85_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_base32_steps.py` (AC1–AC4).
- Assert:
  - `NM&qnZ!91|WMK` for `"Ada"` and `NM&qnZ!91|WMLpoZ+2yDVPj<` for `"Ada Lovelace"`, in that order, each of type `str` (AC1);
  - `NM&qnZ!92MZ^Nq` for `"Zoë"`, equal to `base64.b85encode("Hello, Zoë".encode("utf-8")).decode("ascii")` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_base85("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "NM&qnZ!91|WMK\n", "")`;
    - `"greeting_base85" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_base32`, `greeting_base64`, and `greeting_blake2b`) remains;
    - the exact `greeting_base85` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_base85_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #287 | 2026-10-26 | Initial feature tasks |
