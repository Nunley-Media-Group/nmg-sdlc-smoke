# Tasks: Add greeting_base64 library helper

**Issue**: #209
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_base64

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py` (AC1, AC2, AC3, AC4, FR1, FR2):
  - add `import base64` before `import hashlib`;
  - add `greeting_base64(name: str) -> str` returning `base64.b64encode(greet(name).encode("utf-8")).decode("ascii")`, immediately after `greeting_sha256`.
- In `__init__.py`, add the self-aliased import `from .greet import greeting_base64 as greeting_base64` immediately after `from .greet import greet, greet_many`. Add the `__all__` entry `"greeting_base64"` immediately after `"greet_many"`. Remove no existing export (AC5, FR3).
- In README `## Library` (AC5, FR3):
  - add `greeting_base64,` after `greet_many,` in the import list;
  - add `greeting_base64("Ada")  # "SGVsbG8sIEFkYQ=="` after the `greeting_sha256("Ada")` example, as the last line of the Python block;
  - add the exact `greeting_base64` prose line from design.md after the `greeting_sha256` prose line.

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_base64` to the package-root import list, after `greet_many`.
- Parameterize these cases. For each, assert `type(result) is str` and exact equality (AC1, AC2, AC3):
  - `("Ada", "SGVsbG8sIEFkYQ==")`;
  - `("a?>", "SGVsbG8sIGE/Pg==")`;
  - `("a>>", "SGVsbG8sIGE+Pg==")`;
  - `("Bo", "SGVsbG8sIEJv")`;
  - `("Bob~", "SGVsbG8sIEJvYn4=")`;
  - `("Zo\u00eb", "SGVsbG8sIFpvw6s=")`;
  - `("Zoe\u0308", "SGVsbG8sIFpvZcyI")`;
  - `("A" * 60, "SGVsbG8sIEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQ==")`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC4).
- Assert `"greeting_base64" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_base64("Ada") == "SGVsbG8sIEFkYQ=="` (AC5).
- Run `python -m pytest tests/test_greet.py -k greeting_base64`.

### T003: Exercise five AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_base64_library_helper.feature`, `tests/features/steps/test_greeting_base64_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_base64_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_sha256_steps.py` (AC1–AC5).
- Assert:
  - for `"Ada"` (AC1):
    - the result is exactly `"SGVsbG8sIEFkYQ=="` with `type(result) is str`;
    - `base64.b64decode(result, validate=True) == "Hello, Ada".encode("utf-8")`;
    - that byte string has length 10.
  - for `"a?>"`, `"a>>"`, `"Bo"`, and `"Bob~"` (AC2):
    - the results are exactly `["SGVsbG8sIGE/Pg==", "SGVsbG8sIGE+Pg==", "SGVsbG8sIEJv", "SGVsbG8sIEJvYn4="]`;
    - no result contains `_` or `-`.
  - for `"Zo\u00eb"`, `"Zoe\u0308"`, and `"A" * 60` (AC3):
    - the first two results are exactly `["SGVsbG8sIFpvw6s=", "SGVsbG8sIFpvZcyI"]`;
    - the third is exactly `"SGVsbG8sIEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQ=="`, with length 92 and containing neither `"\n"` nor `"\r"`.
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC4);
  - the README example, exports, and CLI (AC5), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_base64("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "SGVsbG8sIEFkYQ==\n", "")`;
    - `"greeting_base64" in nmg_sdlc_smoke.__all__`;
    - a `PRIOR_EXPORTS` tuple of the 32 names previously in `__all__` is a subset of `nmg_sdlc_smoke.__all__`. The names are `greet`, `greet_many`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_apostrophe`, `greeting_has_ascii_asterisk`, `greeting_has_asterisk`, `greeting_has_at_sign`, `greeting_has_backslash`, `greeting_has_backtick`, `greeting_has_colon`, `greeting_has_dollar`, `greeting_has_double_quote`, `greeting_has_equal`, `greeting_has_exclamation`, `greeting_has_exclamation_or_question`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_plus`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_has_slash`, `greeting_has_underscore`, `greeting_is_ascii`, `greeting_length`, `greeting_reversed`, `greeting_sha256`, `greeting_starts_with_hello`, `greeting_vowel_count`, and `greeting_word_count`;
    - the installed `nmg-smoke` script, resolved through `sysconfig.get_path("scripts")` with an `nmg-smoke.exe` fallback, run with `Ada` gives `(returncode, stdout, stderr) == (0, "Hello, Ada\n", "")`;
    - the exact `greeting_base64` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_base64_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #209 | 2026-10-18 | Initial feature tasks |
