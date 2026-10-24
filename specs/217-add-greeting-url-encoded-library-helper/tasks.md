# Tasks: Add greeting_url_encoded library helper

**Issue**: #217
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_url_encoded

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py` (AC1, AC2, AC3, AC4, FR1, FR2):
  - add `from urllib.parse import quote` immediately after `from collections.abc import Iterable`;
  - add `greeting_url_encoded(name: str) -> str` returning `quote(greet(name), safe="")`, immediately after `greeting_base64`.
- In `__init__.py`, add the self-aliased import `from .greet import greeting_url_encoded as greeting_url_encoded` immediately after the `greeting_starts_with_hello` import, and add the `__all__` entry `"greeting_url_encoded"` immediately after `"greeting_starts_with_hello"`. Remove no existing export (AC5, FR3).
- In README `## Library` (AC5, FR3):
  - add `greeting_url_encoded,` after `greeting_starts_with_hello,` in the import list;
  - add `greeting_url_encoded("Ada")  # "Hello%2C%20Ada"` as the last line of the first Python block;
  - add the exact `greeting_url_encoded` prose line from design.md immediately after the `greeting_base64` prose line.

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_url_encoded` to the package-root import list, after `greeting_starts_with_hello`.
- Parameterize these cases. For each, assert `type(result) is str`, exact equality, and `urllib.parse.unquote(result) == greet(name)` (AC1, AC2, AC3):
  - `("Ada", "Hello%2C%20Ada")`;
  - `("A/B&C~d_e.f", "Hello%2C%20A%2FB%26C~d_e.f")`;
  - `("Zoë", "Hello%2C%20Zo%C3%AB")`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC4).
- Assert `"greeting_url_encoded" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_url_encoded("Ada") == "Hello%2C%20Ada"` (AC5).
- Run `python -m pytest tests/test_greet.py -k greeting_url_encoded`.

### T003: Exercise five AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_url_encoded_library_helper.feature`, `tests/features/steps/test_greeting_url_encoded_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_url_encoded_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_base64_steps.py` (AC1–AC5).
- Assert:
  - for `"Ada"`, the result is exactly `"Hello%2C%20Ada"` with `type(result) is str` (AC1);
  - for `"A/B&C~d_e.f"` and `"Zoë"`, the results are exactly `["Hello%2C%20A%2FB%26C~d_e.f", "Hello%2C%20Zo%C3%AB"]`, and every character of each result is in `A`–`Z`, `a`–`z`, `0`–`9`, `-`, `.`, `_`, `~`, or `%` (AC2);
  - for `"Ada"`, `"Zoë"`, and `"A/B&C~d_e.f"`, `urllib.parse.unquote(library.greeting_url_encoded(name)) == library.greet(name)` (AC3);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC4);
  - the README example, exports, and CLI (AC5), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_url_encoded("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "Hello%2C%20Ada\n", "")`;
    - `"greeting_url_encoded" in nmg_sdlc_smoke.__all__`;
    - a `PRIOR_EXPORTS` tuple of the 33 names previously in `__all__` is a subset of `nmg_sdlc_smoke.__all__`. The names are `greet`, `greet_many`, `greeting_base64`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_apostrophe`, `greeting_has_ascii_asterisk`, `greeting_has_asterisk`, `greeting_has_at_sign`, `greeting_has_backslash`, `greeting_has_backtick`, `greeting_has_colon`, `greeting_has_dollar`, `greeting_has_double_quote`, `greeting_has_equal`, `greeting_has_exclamation`, `greeting_has_exclamation_or_question`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_plus`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_has_slash`, `greeting_has_underscore`, `greeting_is_ascii`, `greeting_length`, `greeting_reversed`, `greeting_sha256`, `greeting_starts_with_hello`, `greeting_vowel_count`, and `greeting_word_count`;
    - the installed `nmg-smoke` script, resolved through `sysconfig.get_path("scripts")` with an `nmg-smoke.exe` fallback, run with `Ada` gives `(returncode, stdout, stderr) == (0, "Hello, Ada\n", "")`;
    - the exact `greeting_url_encoded` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_url_encoded_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #217 | 2026-10-24 | Initial feature tasks |
