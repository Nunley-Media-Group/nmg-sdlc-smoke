# Tasks: Add greeting_shake_128 library helper

**Issue**: #296
**Date**: 2026-11-09
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/284-add-greeting-blake2s-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_shake_128

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_shake_128(name: str) -> str` returning `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)`, immediately after `greeting_blake2s` (AC1, AC2, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_shake_128 as greeting_shake_128` immediately after the `greeting_sha512` import;
  - add the `__all__` entry `"greeting_shake_128"` immediately after `"greeting_sha512"`;
  - remove no existing export (AC3, FR3, FR5).
- In README `## Library`:
  - add `greeting_shake_128,` after `greeting_sha512,` in the import list;
  - add the `greeting_shake_128("Ada")  # "a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774"` example after the `greeting_blake2s("Ada")` example;
  - add the exact `greeting_shake_128` prose line from design.md after the `greeting_blake2s` prose line (AC3, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_shake_128` to the package-root import list after `greeting_sha512`; reuse the existing `hashlib` import, adding it if absent.
- Parameterize `"Ada"` and `"Zoë"` with their exact results from AC1. For each, assert `type(result) is str`, the exact value, `len(result) == 64`, that every character is in `0123456789abcdef`, and equality with `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)` (AC1).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC2).
- Assert `"greeting_shake_128" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_shake_128("Ada") == "a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774"` (AC3).
- Run `python -m pytest tests/test_greet.py -k greeting_shake_128`.

### T003: Exercise three AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_shake_128_library_helper.feature`, `tests/features/steps/test_greeting_shake_128_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the three tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_shake_128_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_blake2s_steps.py` (AC1–AC3).
- Assert:
  - `a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774` for `"Ada"` and `8479a68098ec2f7e622cd2c40a917d3a8b79221a308ebde33c5825dc6f0b4b3f` for `"Zoë"`, in that order, each a 64-character lowercase hex `str` equal to `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)` (AC1);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC2);
  - the README example and unchanged CLI (AC3), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_shake_128("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774\n", "")`;
    - `"greeting_shake_128" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_sha512`, `greeting_space_count`, and `greeting_blake2s`) remains;
    - the exact `greeting_shake_128` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_shake_128_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #296 | 2026-11-09 | Initial feature tasks |
