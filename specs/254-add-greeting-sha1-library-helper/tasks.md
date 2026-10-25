# Tasks: Add greeting_sha1 library helper

**Issue**: #254
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/251-add-greeting-md5-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_sha1

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_sha1(name: str) -> str` returning `hashlib.sha1(greet(name).encode("utf-8")).hexdigest()`, immediately after `greeting_md5`, using the existing `hashlib` import (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_sha1 as greeting_sha1` immediately after the `greeting_rot13` import;
  - add the `__all__` entry `"greeting_sha1"` immediately after `"greeting_rot13"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_sha1,` after `greeting_rot13,` in the import list;
  - add `greeting_sha1("Ada")  # "991f190147e71279d8656214e556b36a22bf73e4"` after the `greeting_md5("Ada")` example;
  - add the exact `greeting_sha1` prose line from design.md after the `greeting_md5` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_sha1` to the package-root import list, after `greeting_rot13`. Keep the existing `import hashlib`.
- Parameterize `("Ada", "991f190147e71279d8656214e556b36a22bf73e4")`, `("Ada Lovelace", "8dde18c21e3195df968018b6213efc61d033ec4f")`, and `("Zoë", "5e2bef193596dd46528fb36c4ef8625f71c84577")` with precomposed U+00EB. For each, assert `type(result) is str` and the exact value (AC1, AC2).
- Assert `greeting_sha1("Zoë") == hashlib.sha1("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_sha1" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_sha1("Ada") == "991f190147e71279d8656214e556b36a22bf73e4"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_sha1`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_sha1_library_helper.feature`, `tests/features/steps/test_greeting_sha1_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_sha1_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_md5_steps.py` (AC1–AC4).
- Assert:
  - results `["991f190147e71279d8656214e556b36a22bf73e4", "8dde18c21e3195df968018b6213efc61d033ec4f"]` for `"Ada"` and `"Ada Lovelace"`, each of type `str` (AC1);
  - result `"5e2bef193596dd46528fb36c4ef8625f71c84577"` for `"Zoë"`, equal to `hashlib.sha1("Hello, Zoë".encode("utf-8")).hexdigest()` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_sha1("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "991f190147e71279d8656214e556b36a22bf73e4\n", "")`;
    - `"greeting_sha1" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_md5` and `greeting_sha256`) remains;
    - the exact `greeting_sha1` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_sha1_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #254 | 2026-10-25 | Initial feature tasks |
