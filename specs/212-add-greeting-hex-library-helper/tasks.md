# Tasks: Add greeting_hex library helper

**Issue**: #212
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/209-add-greeting-base64-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_hex

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_hex(name: str) -> str` returning `greet(name).encode("utf-8").hex()`, immediately after `greeting_base64` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_hex as greeting_hex` immediately after the `greeting_has_underscore` import. Add the `__all__` entry `"greeting_hex"` immediately after `"greeting_has_underscore"`. Remove no existing export (AC4, FR3).
- In README `## Library` (AC4, FR3):
  - add `greeting_hex,` after `greeting_has_underscore,` in the import list;
  - add `greeting_hex("Ada")  # "48656c6c6f2c20416461"` after the `greeting_base64("Ada")` example, as the last line of the Python block;
  - add the exact `greeting_hex` prose line from design.md after the `greeting_base64` prose line.

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_hex` to the package-root import list, after `greeting_has_underscore`.
- Parameterize these cases. For each, assert `type(result) is str`, exact equality, `len(result) == 2 * len(greet(name).encode("utf-8"))`, and `set(result) <= set("0123456789abcdef")` (AC1, AC2):
  - `("Ada", "48656c6c6f2c20416461")`;
  - `("Zoë", "48656c6c6f2c205a6fc3ab")`;
  - `("Zoë", "48656c6c6f2c205a6f65cc88")`;
  - `("é中", "48656c6c6f2c20c3a9e4b8ad")`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_hex" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_hex("Ada") == "48656c6c6f2c20416461"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_hex`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_hex_library_helper.feature`, `tests/features/steps/test_greeting_hex_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_hex_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_base64_steps.py` (AC1–AC4).
- Assert:
  - for `"Ada"` (AC1):
    - the result is exactly `"48656c6c6f2c20416461"` with `type(result) is str`;
    - `len(result) == 20 == 2 * len("Hello, Ada".encode("utf-8"))`;
    - `bytes.fromhex(result) == "Hello, Ada".encode("utf-8")`.
  - for `"Zoë"`, `"Zoë"`, and `"é中"` (AC2):
    - the results are exactly `["48656c6c6f2c205a6fc3ab", "48656c6c6f2c205a6f65cc88", "48656c6c6f2c20c3a9e4b8ad"]`;
    - every result satisfies `set(result) <= set("0123456789abcdef")`.
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example, exports, and CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_hex("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "48656c6c6f2c20416461\n", "")`;
    - `"greeting_hex" in nmg_sdlc_smoke.__all__`;
    - a `PRIOR_EXPORTS` tuple of the 38 names previously in `__all__` is a subset of `nmg_sdlc_smoke.__all__`. The names are `greet`, `greet_many`, `greeting_base64`, `greeting_bytes`, `greeting_casefold`, `greeting_digit_count`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_apostrophe`, `greeting_has_ascii_asterisk`, `greeting_has_asterisk`, `greeting_has_at_sign`, `greeting_has_backslash`, `greeting_has_backtick`, `greeting_has_colon`, `greeting_has_dollar`, `greeting_has_double_quote`, `greeting_has_equal`, `greeting_has_exclamation`, `greeting_has_exclamation_or_question`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_plus`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_has_slash`, `greeting_has_underscore`, `greeting_is_ascii`, `greeting_length`, `greeting_lowercase_count`, `greeting_punctuation_count`, `greeting_reversed`, `greeting_sha256`, `greeting_space_count`, `greeting_starts_with_hello`, `greeting_uppercase_count`, `greeting_vowel_count`, and `greeting_word_count`;
    - the installed `nmg-smoke` script, resolved through `sysconfig.get_path("scripts")` with an `nmg-smoke.exe` fallback, run with `Ada` gives `(returncode, stdout, stderr) == (0, "Hello, Ada\n", "")`;
    - the exact `greeting_hex` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_hex_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #212 | 2026-10-24 | Initial feature tasks |
