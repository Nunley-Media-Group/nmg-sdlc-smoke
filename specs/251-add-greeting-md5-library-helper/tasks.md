# Tasks: Add greeting_md5 library helper

**Issue**: #251
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/206-add-greeting-sha256-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_md5

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_md5(name: str) -> str` returning `hashlib.md5(greet(name).encode("utf-8")).hexdigest()`, immediately after `greeting_sha256`, using the existing `hashlib` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_md5 as greeting_md5` immediately after the `greeting_lowercase_count` import;
  - add the `__all__` entry `"greeting_md5"` immediately after `"greeting_lowercase_count"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_md5,` after `greeting_lowercase_count,` in the import list;
  - add `greeting_md5("Ada")  # "a4f502ca98cce831af61b0fe0a319382"` after the `greeting_sha256("Ada")` example;
  - add the exact `greeting_md5` prose line from design.md after the `greeting_sha256` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `import hashlib` to the standard-library imports. Add `greeting_md5` to the package-root import list, after `greeting_lowercase_count`.
- Parameterize `("Ada", "a4f502ca98cce831af61b0fe0a319382")`, `("Ada Lovelace", "bd0b2e5ea5baf6775e93262ce37d5a4a")`, and `("Zoë", "26ed66c6559b1e033c70ef2301fe0beb")` with precomposed U+00EB. For each, assert `type(result) is str` and the exact value (AC1, AC2).
- Assert `greeting_md5("Zoë") == hashlib.md5("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_md5" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_md5("Ada") == "a4f502ca98cce831af61b0fe0a319382"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_md5`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_md5_library_helper.feature`, `tests/features/steps/test_greeting_md5_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_md5_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_adler32_steps.py` (AC1–AC4).
- Assert:
  - results `["a4f502ca98cce831af61b0fe0a319382", "bd0b2e5ea5baf6775e93262ce37d5a4a"]` for `"Ada"` and `"Ada Lovelace"`, each of type `str` (AC1);
  - result `"26ed66c6559b1e033c70ef2301fe0beb"` for `"Zoë"`, equal to `hashlib.md5("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_md5("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "a4f502ca98cce831af61b0fe0a319382\n", "")`;
    - `"greeting_md5" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_adler32` and `greeting_sha256`) remains;
    - the exact `greeting_md5` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_md5_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #251 | 2026-10-25 | Initial feature tasks |
