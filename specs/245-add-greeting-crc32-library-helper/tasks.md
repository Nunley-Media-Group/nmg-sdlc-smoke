# Tasks: Add greeting_crc32 library helper

**Issue**: #245
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/206-add-greeting-sha256-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_crc32

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`:
  - add `import zlib` after `import string`;
  - add `greeting_crc32(name: str) -> int` returning `zlib.crc32(greet(name).encode("utf-8"))`, immediately after `greeting_url_encoded` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_crc32 as greeting_crc32` and the `__all__` entry `"greeting_crc32"`, each immediately after its `greeting_casefold` entry. Remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_crc32,` after `greeting_casefold,` in the import list;
  - add `greeting_crc32("Ada")  # 2761732226` after the `greeting_rot13("Ada")  # "Uryyb, Nqn"` example;
  - add the exact `greeting_crc32` prose line from design.md after the `greeting_url_encoded` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_crc32` to the package-root import list, after `greeting_casefold`.
- Parameterize `("Ada", 2761732226)`, `("Ada Lovelace", 2495651459)`, and `("Zoë", 2271742533)` with precomposed U+00EB. For each, assert `type(result) is int` and the exact value (AC1, AC2).
- Assert `greeting_crc32("Zoë") == zlib.crc32("Hello, Zoë".encode("utf-8"))` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_crc32" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_crc32("Ada") == 2761732226` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_crc32`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_crc32_library_helper.feature`, `tests/features/steps/test_greeting_crc32_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_crc32_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_sha256_steps.py` (AC1–AC4).
- Assert:
  - results `[2761732226, 2495651459]` for `"Ada"` and `"Ada Lovelace"`, each of type `int` (AC1);
  - result `2271742533` for `"Zoë"`, equal to `zlib.crc32("Hello, Zoë".encode("utf-8"))` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_crc32("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "2761732226\n", "")`;
    - `"greeting_crc32" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_letter_count` and `greeting_url_encoded`) remains;
    - the exact `greeting_crc32` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_crc32_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #245 | 2026-10-25 | Initial feature tasks |
