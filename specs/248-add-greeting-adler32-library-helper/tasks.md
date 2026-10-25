# Tasks: Add greeting_adler32 library helper

**Issue**: #248
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/245-add-greeting-crc32-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_adler32

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_adler32(name: str) -> int` returning `zlib.adler32(greet(name).encode("utf-8"))`, immediately after `greeting_crc32`, using the existing `zlib` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_adler32 as greeting_adler32` immediately after `from .greet import greet, greet_many`;
  - add the `__all__` entry `"greeting_adler32"` immediately after `"greet_many"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_adler32,` after `greet_many,` in the import list;
  - add `greeting_adler32("Ada")  # 312279879` after the `greeting_crc32("Ada")  # 2761732226` example;
  - add the exact `greeting_adler32` prose line from design.md after the `greeting_crc32` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_adler32` to the package-root import list, after `greet_many`.
- Parameterize `("Ada", 312279879)`, `("Ada Lovelace", 1063257746)`, and `("Zoë", 400032888)` with precomposed U+00EB. For each, assert `type(result) is int` and the exact value (AC1, AC2).
- Assert `greeting_adler32("Zoë") == zlib.adler32("Hello, Zoë".encode("utf-8"))` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_adler32" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_adler32("Ada") == 312279879` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_adler32`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_adler32_library_helper.feature`, `tests/features/steps/test_greeting_adler32_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_adler32_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_crc32_steps.py` (AC1–AC4).
- Assert:
  - results `[312279879, 1063257746]` for `"Ada"` and `"Ada Lovelace"`, each of type `int` (AC1);
  - result `400032888` for `"Zoë"`, equal to `zlib.adler32("Hello, Zoë".encode("utf-8"))` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_adler32("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "312279879\n", "")`;
    - `"greeting_adler32" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_crc32` and `greeting_letter_count`) remains;
    - the exact `greeting_adler32` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_adler32_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #248 | 2026-10-25 | Initial feature tasks |
