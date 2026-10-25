# Tasks: Add greeting_sha3_512 library helper

**Issue**: #272
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/269-add-greeting-sha3-256-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_sha3_512

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_sha3_512(name: str) -> str` returning `hashlib.sha3_512(greet(name).encode("utf-8")).hexdigest()`, immediately after `greeting_sha3_256`, using the existing `hashlib` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_sha3_512 as greeting_sha3_512` immediately after the `greeting_sha3_256` import;
  - add the `__all__` entry `"greeting_sha3_512"` immediately after `"greeting_sha3_256"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_sha3_512,` after `greeting_sha3_256,` in the import list;
  - add the `greeting_sha3_512("Ada")` example with the AC1 `Ada` digest after the `greeting_sha3_256("Ada")` example;
  - add the exact `greeting_sha3_512` prose line from design.md after the `greeting_sha3_256` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_sha3_512` to the package-root import list, after `greeting_sha3_256`. Keep the existing `import hashlib`.
- Parameterize `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` (precomposed U+00EB) with their exact digests from AC1 and AC2. For each, assert `type(result) is str` and the exact value (AC1, AC2).
- Assert `greeting_sha3_512("Zoë") == hashlib.sha3_512("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_sha3_512" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_sha3_512("Ada")` equals the AC1 `Ada` digest (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_sha3_512`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_sha3_512_library_helper.feature`, `tests/features/steps/test_greeting_sha3_512_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_sha3_512_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_sha3_256_steps.py` (AC1–AC4).
- Assert:
  - the exact AC1 digests for `"Ada"` and `"Ada Lovelace"`, in that order, each of type `str` (AC1);
  - the exact AC2 digest for `"Zoë"`, equal to `hashlib.sha3_512("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_sha3_512("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "<AC1 Ada digest>\n", "")`;
    - `"greeting_sha3_512" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_sha3_256` and `greeting_sha512`) remains;
    - the exact `greeting_sha3_512` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_sha3_512_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #272 | 2026-10-25 | Initial feature tasks |
