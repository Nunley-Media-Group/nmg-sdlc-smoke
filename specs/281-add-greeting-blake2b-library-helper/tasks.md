# Tasks: Add greeting_blake2b library helper

**Issue**: #281
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/278-add-greeting-sha3-224-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_blake2b

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_blake2b(name: str) -> str` returning `hashlib.blake2b(greet(name).encode("utf-8")).hexdigest()`, immediately after `greeting_sha3_512` and before `greeting_base32`, using the existing `hashlib` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_blake2b as greeting_blake2b` immediately after the `greeting_base64` import;
  - add the `__all__` entry `"greeting_blake2b"` immediately after `"greeting_base64"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_blake2b,` after `greeting_base64,` in the import list;
  - add the `greeting_blake2b("Ada")` example with the AC1 `Ada` digest after the `greeting_sha3_512("Ada")` example;
  - add the exact `greeting_blake2b` prose line from design.md after the `greeting_sha3_512` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_blake2b` to the package-root import list, after `greeting_base64`. Keep the existing `import hashlib`.
- Parameterize `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` (precomposed U+00EB) with their exact digests from AC1 and AC2. For each, assert `type(result) is str`, `len(result) == 128`, and the exact value (AC1, AC2).
- Assert `greeting_blake2b("Zoë") == hashlib.blake2b("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_blake2b" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_blake2b("Ada")` equals the AC1 `Ada` digest (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_blake2b`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_blake2b_library_helper.feature`, `tests/features/steps/test_greeting_blake2b_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_blake2b_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_sha3_224_steps.py` (AC1–AC4).
- Assert:
  - the exact AC1 digests for `"Ada"` and `"Ada Lovelace"`, in that order, each of type `str` (AC1);
  - the exact AC2 digest for `"Zoë"`, equal to `hashlib.blake2b("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_blake2b("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "<AC1 Ada digest>\n", "")`;
    - `"greeting_blake2b" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_base64`, `greeting_bytes`, `greeting_sha3_224`, and `greeting_sha3_512`) remains;
    - the exact `greeting_blake2b` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_blake2b_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #281 | 2026-10-25 | Initial feature tasks |
