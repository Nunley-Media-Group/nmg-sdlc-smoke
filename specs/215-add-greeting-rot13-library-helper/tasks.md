# Tasks: Add greeting_rot13 library helper

**Issue**: #215
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_rot13

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py` (AC1, AC2, AC3, AC4, FR1, FR2):
  - add `import codecs` immediately after `import base64`;
  - add `greeting_rot13(name: str) -> str` returning `codecs.encode(greet(name), "rot13")`, immediately after `greeting_base64`.
- In `__init__.py`, add the self-aliased import `from .greet import greeting_rot13 as greeting_rot13` immediately after the `greeting_reversed` import, and add the `__all__` entry `"greeting_rot13"` immediately after `"greeting_reversed"`. Remove no existing export (AC5, FR3).
- In README `## Library` (AC5, FR3):
  - add `greeting_rot13,` after `greeting_reversed,` in the import list;
  - add `greeting_rot13("Ada")  # "Uryyb, Nqn"` as the last line of the first Python block;
  - add the exact `greeting_rot13` prose line from design.md immediately after the `greeting_base64` prose line.

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_rot13` to the package-root import list, after `greeting_reversed`.
- Parameterize these cases. For each, assert `type(result) is str`, exact equality, and `codecs.encode(result, "rot13") == greet(name)` (AC1, AC2, AC3):
  - `("Ada", "Uryyb, Nqn")`;
  - `("Mary-Jane O'Neil", "Uryyb, Znel-Wnar B'Arvy")`;
  - `("Zoë", "Uryyb, Mbë")`;
  - `("Ｚed 42", "Uryyb, Ｚrq 42")`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC4).
- Assert `"greeting_rot13" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_rot13("Ada") == "Uryyb, Nqn"` (AC5).
- Run `python -m pytest tests/test_greet.py -k greeting_rot13`.

### T003: Exercise five AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_rot13_library_helper.feature`, `tests/features/steps/test_greeting_rot13_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_rot13_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_base64_steps.py` (AC1–AC5).
- Assert:
  - for `"Ada"`, the result is exactly `"Uryyb, Nqn"` with `type(result) is str` (AC1);
  - for `"Mary-Jane O'Neil"`, `"Zoë"`, and `"Ｚed 42"`, the results are exactly `["Uryyb, Znel-Wnar B'Arvy", "Uryyb, Mbë", "Uryyb, Ｚrq 42"]`, and every character of each greeting that is not an ASCII letter appears unchanged at the same index of its result (AC2);
  - for `"Ada"`, `"Zoë"`, and `"Mary-Jane O'Neil"`, `codecs.encode(library.greeting_rot13(name), "rot13") == library.greet(name)` (AC3);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC4);
  - the README example, exports, and CLI (AC5), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_rot13("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "Uryyb, Nqn\n", "")`;
    - `"greeting_rot13" in nmg_sdlc_smoke.__all__`;
    - a `PRIOR_EXPORTS` tuple of the 33 names previously in `__all__` is a subset of `nmg_sdlc_smoke.__all__`. The names are `greet`, `greet_many`, `greeting_base64`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_apostrophe`, `greeting_has_ascii_asterisk`, `greeting_has_asterisk`, `greeting_has_at_sign`, `greeting_has_backslash`, `greeting_has_backtick`, `greeting_has_colon`, `greeting_has_dollar`, `greeting_has_double_quote`, `greeting_has_equal`, `greeting_has_exclamation`, `greeting_has_exclamation_or_question`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_plus`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_has_slash`, `greeting_has_underscore`, `greeting_is_ascii`, `greeting_length`, `greeting_reversed`, `greeting_sha256`, `greeting_starts_with_hello`, `greeting_vowel_count`, and `greeting_word_count`;
    - the installed `nmg-smoke` script, resolved through `sysconfig.get_path("scripts")` with an `nmg-smoke.exe` fallback, run with `Ada` gives `(returncode, stdout, stderr) == (0, "Hello, Ada\n", "")`;
    - the exact `greeting_rot13` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_rot13_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #215 | 2026-10-24 | Initial feature tasks |
