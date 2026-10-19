# Tasks: Add greeting_sha256 library helper

**Issue**: #206
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_sha256

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `import hashlib` before `from collections.abc import Iterable`. Add `greeting_sha256(name: str) -> str` returning `hashlib.sha256(greet(name).encode("utf-8")).hexdigest()`, immediately after `greeting_vowel_count` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`, add the self-aliased import `from .greet import greeting_sha256 as greeting_sha256` and the `__all__` entry `"greeting_sha256"`, each immediately after its `greeting_reversed` entry. Remove no existing export (AC4, FR3).
- In README `## Library` (AC4, FR3):
  - add `greeting_sha256,` after `greeting_reversed,` in the import list;
  - add `greeting_sha256("Ada")  # "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"` after the `greeting_vowel_count("Ada")  # 4` example;
  - add the exact `greeting_sha256` prose line from design.md after the `greeting_vowel_count` prose line.

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_sha256` to the package-root import list, after `greeting_reversed`.
- Parameterize these cases. For each, assert `type(result) is str` and exact equality (AC1, AC2):
  - `("Ada", "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66")`;
  - `("Zo\u00eb", "aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524")`;
  - `("Zoe\u0308", "af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064")`.
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_sha256" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_sha256("Ada") == "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_sha256`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_sha256_library_helper.feature`, `tests/features/steps/test_greeting_sha256_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_sha256_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_vowel_count_steps.py` and `tests/features/steps/test_greeting_reversed_steps.py` (AC1–AC4).
- Assert:
  - for `"Ada"` (AC1):
    - the result is exactly `"7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"` with `type(result) is str`;
    - `len("Hello, Ada".encode("utf-8")) == 10`;
    - the result equals `hashlib.sha256("Hello, Ada".encode("utf-8")).hexdigest()`;
    - the result has length 64, and every character is in `0123456789abcdef`.
  - results `["aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524", "af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064"]` for `"Zo\u00eb"` and `"Zoe\u0308"` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example, exports, and CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_sha256("Ada"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66\n", "")`;
    - `"greeting_sha256" in nmg_sdlc_smoke.__all__`;
    - a `PRIOR_EXPORTS` tuple of the 31 names previously in `__all__` is a subset of `nmg_sdlc_smoke.__all__`. The names are `greet`, `greet_many`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_apostrophe`, `greeting_has_ascii_asterisk`, `greeting_has_asterisk`, `greeting_has_at_sign`, `greeting_has_backslash`, `greeting_has_backtick`, `greeting_has_colon`, `greeting_has_dollar`, `greeting_has_double_quote`, `greeting_has_equal`, `greeting_has_exclamation`, `greeting_has_exclamation_or_question`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_plus`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_has_slash`, `greeting_has_underscore`, `greeting_is_ascii`, `greeting_length`, `greeting_reversed`, `greeting_starts_with_hello`, `greeting_vowel_count`, and `greeting_word_count`;
    - the installed `nmg-smoke` script, resolved through `sysconfig.get_path("scripts")` with an `nmg-smoke.exe` fallback, run with `Ada` gives `(returncode, stdout, stderr) == (0, "Hello, Ada\n", "")`;
    - the exact `greeting_sha256` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_sha256_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #206 | 2026-10-18 | Initial feature tasks |
