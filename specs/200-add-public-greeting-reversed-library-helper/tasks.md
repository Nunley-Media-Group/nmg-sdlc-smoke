# Tasks: Add public greeting_reversed library helper

**Issue**: #200
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_reversed

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- Add `greeting_reversed(name: str) -> str` returning `greet(name)[::-1]` immediately after `greeting_casefold` in `greet.py` (AC1, AC2, FR1, FR2).
- Add the self-aliased package import `from .greet import greeting_reversed as greeting_reversed` and the `__all__` entry `"greeting_reversed"`, each immediately after the `greeting_length` entry. Remove no existing export (AC3, FR3).
- In README `## Library`:
  - add `greeting_reversed,` after `greeting_length,` in the import list;
  - add `greeting_reversed("Ada")  # "adA ,olleH"` after the `greeting_casefold("Straße")` example;
  - add the code-point/validation prose line from design.md after the `greeting_casefold` prose line (FR5).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_reversed` to the package-root import list after `greeting_length`. Assert `greeting_reversed("Ada") == "adA ,olleH"` and `greeting_reversed("Zo\u00eb") == "\u00eboZ ,olleH"` (exactly `"ëoZ ,olleH"` with U+00EB) (AC1).
- Parameterize `""`, `"   "`, and `None`. Assert `pytest.raises(ValueError, match="^name must not be blank$")` for each (AC2).
- Assert:
  - `"greeting_reversed" in nmg_sdlc_smoke.__all__`;
  - a hard-coded list of the 29 names in `__all__` before this change (`"greet"` through `"greeting_word_count"`) is a subset of `nmg_sdlc_smoke.__all__`;
  - `greet("Ada") == "Hello, Ada"` (AC3).
- Run `python -m pytest tests/test_greet.py -k greeting_reversed`.

### T003: Exercise three AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_public_greeting_reversed_library_helper.feature`, `tests/features/steps/test_greeting_reversed_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the three tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments. Implement deterministic steps with `scenarios("../add_public_greeting_reversed_library_helper.feature")` and public `nmg_sdlc_smoke` imports, following `tests/features/steps/test_casefold_steps.py` (AC1–AC3).
- Assert:
  - exact results `"adA ,olleH"` and `"ëoZ ,olleH"` (AC1);
  - `ValueError` with exact message `name must not be blank` for `""`, `"   "`, and `None` (AC2);
  - `"greeting_reversed" in nmg_sdlc_smoke.__all__` and the 29 prior `__all__` names still listed;
  - `greet("Ada") == "Hello, Ada"`;
  - the installed `nmg-smoke` script (resolved through `sysconfig.get_path("scripts")`, with `nmg-smoke.exe` fallback) run with `Ada` gives `(returncode, stdout, stderr) == (0, "Hello, Ada\n", "")` (AC3).
- Run `python -m pytest tests/features/steps/test_greeting_reversed_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #200 | 2026-10-06 | Initial feature tasks |
