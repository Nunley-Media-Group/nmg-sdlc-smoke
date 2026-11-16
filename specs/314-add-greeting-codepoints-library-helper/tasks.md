# Tasks: Add greeting_codepoints library helper

**Issue**: #314
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/311-add-greeting-swapcase-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_codepoints

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_codepoints(name: str) -> list[int]` returning `[ord(ch) for ch in greet(name)]` immediately after `greeting_bytes` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_codepoints as greeting_codepoints` immediately after the `greeting_casefold` import;
  - add the `__all__` entry `"greeting_codepoints"` immediately after `"greeting_casefold"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_codepoints,` after `greeting_casefold,` in the import list;
  - add the `greeting_codepoints("Ada")  # [72, 101, 108, 108, 111, 44, 32, 65, 100, 97]` example after the `greeting_bytes("Ada")  # 10` example;
  - add the exact `greeting_codepoints` prose line from design.md after the `greeting_casefold` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_codepoints` to the package-root import list after `greeting_casefold`.
- Parameterize `("Ada", [72, 101, 108, 108, 111, 44, 32, 65, 100, 97])` and `("Zoë", [72, 101, 108, 108, 111, 44, 32, 90, 111, 235])`. For each, assert the result is a `list`, every element is an `int`, the result equals the expected value, and it equals `[ord(ch) for ch in greet(name)]` (AC1).
- Assert `greeting_codepoints("\U0001F600") == [72, 101, 108, 108, 111, 44, 32, 128512]` and `len(greeting_codepoints("\U0001F600")) == greeting_length("\U0001F600")` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_codepoints" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_codepoints("Ada") == [72, 101, 108, 108, 111, 44, 32, 65, 100, 97]` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_codepoints`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_codepoints_library_helper.feature`, `tests/features/steps/test_greeting_codepoints_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_codepoints_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_swapcase_steps.py` (AC1–AC4).
- Assert:
  - `[72, 101, 108, 108, 111, 44, 32, 65, 100, 97]` and `[72, 101, 108, 108, 111, 44, 32, 90, 111, 235]` for `"Ada"` and `"Zoë"`, each a `list[int]` equal to `[ord(ch) for ch in greet(name)]` (AC1);
  - `[72, 101, 108, 108, 111, 44, 32, 128512]` for `"\U0001F600"`, with length equal to `greeting_length("\U0001F600")` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_codepoints("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "[72, 101, 108, 108, 111, 44, 32, 65, 100, 97]\n", "")`;
    - `"greeting_codepoints" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_casefold`, `greeting_bytes`, and `greeting_crc32`) remains;
    - the exact `greeting_codepoints` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_codepoints_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #314 | 2026-11-15 | Initial feature tasks |
