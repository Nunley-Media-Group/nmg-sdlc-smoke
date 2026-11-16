# Tasks: Add greeting_utf16_length library helper

**Issue**: #317
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/314-add-greeting-codepoints-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_utf16_length

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_utf16_length(name: str) -> int` returning `len(greet(name).encode("utf-16-le")) // 2` immediately after `greeting_codepoints` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_utf16_length as greeting_utf16_length` immediately after the `greeting_url_encoded` import;
  - add the `__all__` entry `"greeting_utf16_length"` immediately after `"greeting_url_encoded"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_utf16_length,` after `greeting_uppercase_count,` in the import list;
  - add the `greeting_utf16_length("Ada")  # 10` example after the `greeting_codepoints("Ada")` example;
  - add the exact `greeting_utf16_length` prose line from design.md after the `greeting_codepoints` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_utf16_length` to the package-root import list.
- Parameterize `"Ada"` and `"Zoë"`. For each, assert the result is an `int`, equals `10`, and equals `len(greet(name).encode("utf-16-le")) // 2` (AC1).
- Assert `greeting_utf16_length("\U0001F600") == 9` and `greeting_utf16_length("\U0001F600") == greeting_length("\U0001F600") + 1` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_utf16_length" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_utf16_length("Ada") == 10` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_utf16_length`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_utf16_length_library_helper.feature`, `tests/features/steps/test_greeting_utf16_length_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_utf16_length_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_codepoints_steps.py` (AC1–AC4).
- Assert:
  - `10` for both `"Ada"` and `"Zoë"`, each an `int` equal to `len(greet(name).encode("utf-16-le")) // 2` (AC1);
  - `9` for `"\U0001F600"`, equal to `greeting_length("\U0001F600") + 1` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_utf16_length("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "10\n", "")`;
    - `"greeting_utf16_length" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_url_encoded`, `greeting_codepoints`, and `greeting_vowel_count`) remains;
    - the exact `greeting_utf16_length` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_utf16_length_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #317 | 2026-11-15 | Initial feature tasks |
