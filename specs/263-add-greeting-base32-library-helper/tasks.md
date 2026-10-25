# Tasks: Add greeting_base32 library helper

**Issue**: #263
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/209-add-greeting-base64-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_base32

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_base32(name: str) -> str` returning `base64.b32encode(greet(name).encode("utf-8")).decode("ascii")`, immediately before `greeting_base64`, using the existing `base64` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_base32 as greeting_base32` immediately after the `greeting_adler32` import;
  - add the `__all__` entry `"greeting_base32"` immediately after `"greeting_adler32"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_base32,` after `greeting_adler32,` in the import list;
  - add the `greeting_base32("Ada")  # "JBSWY3DPFQQECZDB"` example after the `greeting_base64("Ada")` example;
  - add the exact `greeting_base32` prose line from design.md after the `greeting_base64` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `import base64` to the module imports, and add `greeting_base32` to the package-root import list after `greeting_adler32`.
- Parameterize `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` (precomposed U+00EB) with their exact results from AC1 and AC2. For each, assert `type(result) is str` and the exact value (AC1, AC2).
- Assert `greeting_base32("Zoë") == base64.b32encode("Hello, Zoë".encode("utf-8")).decode("ascii")` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_base32" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_base32("Ada") == "JBSWY3DPFQQECZDB"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_base32`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_base32_library_helper.feature`, `tests/features/steps/test_greeting_base32_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_base32_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_base64_steps.py` (AC1–AC4).
- Assert:
  - `JBSWY3DPFQQECZDB` for `"Ada"` and `JBSWY3DPFQQECZDBEBGG65TFNRQWGZI=` for `"Ada Lovelace"`, in that order, each of type `str` (AC1);
  - `JBSWY3DPFQQFU36DVM======` for `"Zoë"`, equal to `base64.b32encode("Hello, Zoë".encode("utf-8")).decode("ascii")` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_base32("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "JBSWY3DPFQQECZDB\n", "")`;
    - `"greeting_base32" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_adler32` and `greeting_base64`) remains;
    - the exact `greeting_base32` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_base32_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #263 | 2026-10-25 | Initial feature tasks |
