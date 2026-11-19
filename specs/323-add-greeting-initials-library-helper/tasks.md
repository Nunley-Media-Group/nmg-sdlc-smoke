# Tasks: Add greeting_initials library helper

**Issue**: #323
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/319-add-greeting-words-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_initials

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_initials(name: str) -> str` returning `"".join(word[0] for word in greeting_words(name))` immediately after `greeting_words` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_initials as greeting_initials` immediately after the `greeting_html_escaped` import;
  - add the `__all__` entry `"greeting_initials"` immediately after `"greeting_html_escaped"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_initials,` after `greeting_html_escaped,` in the import list;
  - add the `greeting_initials("Ada Lovelace")  # "HAL"` example after the `greeting_words("Ada")  # ['Hello,', 'Ada']` example;
  - add the exact `greeting_initials` prose line from design.md after the `greeting_words` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_initials` to the package-root import list after `greeting_html_escaped`.
- Parameterize `("Ada", "HA")` and `("Zoë", "HZ")`. For each, assert the result is a `str` and equals the expected value (AC1).
- Parameterize `("Ada Lovelace", "HAL")`, `("Ada \t Lovelace", "HAL")`, and `("ada lovelace", "Hal")`. For each, assert the result equals the expected value and its length equals `greeting_word_count(name)` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_initials" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_initials("Ada") == "HA"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_initials`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_initials_library_helper.feature`, `tests/features/steps/test_greeting_initials_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_initials_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_words_steps.py` (AC1–AC4).
- Assert:
  - `"HA"` and `"HZ"` for `"Ada"` and `"Zoë"`, each of type `str` (AC1);
  - `"HAL"`, `"HAL"`, and `"Hal"` for `"Ada Lovelace"`, `"Ada \t Lovelace"`, and `"ada lovelace"`, each with length equal to `greeting_word_count(name)` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_initials("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "HA\n", "")`;
    - `"greeting_initials" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_words`, `greeting_word_count`, `greeting_utf16_length`, and `greeting_html_escaped`) remains;
    - the exact `greeting_initials` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_initials_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #323 | 2026-11-19 | Initial feature tasks |
