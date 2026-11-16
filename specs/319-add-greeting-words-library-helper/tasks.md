# Tasks: Add greeting_words library helper

**Issue**: #319
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/93-add-greeting-word-count-lifecycle-fixture/

## Implementation Tasks

### T001: Implement, export, and document greeting_words

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_words(name: str) -> list[str]` returning `greet(name).split()` immediately after `greeting_word_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_words as greeting_words` immediately after the `greeting_word_count` import;
  - add the `__all__` entry `"greeting_words"` immediately after `"greeting_word_count"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_words,` after `greeting_word_count,` in the import list;
  - add the `greeting_words("Ada")  # ['Hello,', 'Ada']` example after the `greeting_word_count("Ada Lovelace")  # 3` example;
  - add the exact `greeting_words` prose line from design.md after the `greeting_word_count` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_words` to the package-root import list after `greeting_word_count`.
- Parameterize `("Ada", ["Hello,", "Ada"])` and `("Zoë", ["Hello,", "Zoë"])`. For each, assert the result is a `list`, every element is a `str`, the result equals the expected value, and it equals `greet(name).split()` (AC1).
- Parameterize `"Ada Lovelace"` and `"Ada \t Lovelace"`. For each, assert the result equals `["Hello,", "Ada", "Lovelace"]` and its length equals `greeting_word_count(name)` (AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_words" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_words("Ada") == ["Hello,", "Ada"]` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_words`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_words_library_helper.feature`, `tests/features/steps/test_greeting_words_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_words_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_swapcase_steps.py` (AC1–AC4).
- Assert:
  - `["Hello,", "Ada"]` and `["Hello,", "Zoë"]` for `"Ada"` and `"Zoë"`, each a `list[str]` equal to `greet(name).split()` (AC1);
  - `["Hello,", "Ada", "Lovelace"]` for both `"Ada Lovelace"` and `"Ada \t Lovelace"`, each with length equal to `greeting_word_count(name)` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_words("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "['Hello,', 'Ada']\n", "")`;
    - `"greeting_words" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_word_count`, `greeting_vowel_count`, and `greeting_swapcase`) remains;
    - the exact `greeting_words` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_words_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #319 | 2026-11-15 | Initial feature tasks |
