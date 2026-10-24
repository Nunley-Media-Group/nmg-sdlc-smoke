# Design: Add greeting_consonant_count library helper

**Issue**: #213
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/203-add-greeting-vowel-count-library-helper/

## Overview

The helper mirrors `greeting_vowel_count`. It calls `greet(name)`, which validates the name, then counts the characters of the completed greeting that belong to an exact 42-character ASCII consonant literal. The helper is exported from the package root and documented in the README Library section. No new module, constant, or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_vowel_count`, separated from its neighbors by two blank lines:

```python
def greeting_consonant_count(name: str) -> int:
    return sum(
        character in "bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ"
        for character in greet(name)
    )
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** The helper compares each single code point of the Python `str` against exactly the 21 lowercase and 21 uppercase ASCII consonants, `y`/`Y` included. There is no case conversion and no Unicode normalization.
  - Vowels, digits, whitespace, and punctuation are not counted.
  - Precomposed accented letters such as U+00C9 are not counted.
  - Fullwidth letters such as U+FF22 are not counted.
- **Return type.** `sum` over booleans starts at the `int` `0`, so the result is a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_consonant_count as greeting_consonant_count` immediately after the `greeting_casefold` import line;
- add `"greeting_consonant_count"` to `__all__` immediately after `"greeting_casefold"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_consonant_count,` to the import list immediately after `greeting_casefold,`;
- add the example `greeting_consonant_count("Ada")  # 4` immediately after `greeting_vowel_count("Ada")  # 4`;
- add this exact prose line immediately after the `greeting_vowel_count` prose line:

```markdown
`greeting_consonant_count` counts the 42 ASCII consonant letters (every letter `A`–`Z` and `a`–`z` except `a e i o u A E I O U`, so `y` and `Y` count) in the complete greeting (not the name alone); vowels, digits, spaces, punctuation, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_consonant_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_consonant_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_consonant_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts the 42 ASCII consonant code points in `greet(name)`: `"Ada"` → `4`, all 42 consonants → `45`, `"Ady"` → `5`, `"Yy"` → `5`, `"Bob 42!"` → `5`, `"Émile"` (U+00C9) → `5`, `"Ｂｃｄ"` (U+FF22 U+FF43 U+FF44) → `3` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Membership test against an explicit 42-character consonant literal | Selected | Gives an exact code-point contract, matches the `greeting_vowel_count` idiom, and uses only the standard library |
| `character.isascii() and character.isalpha() and character not in "aeiouAEIOU"` | Rejected | Equivalent behavior, but more indirect than the sibling helper's literal set |
| `casefold()`/`lower()` before matching | Rejected | Case conversion can map non-ASCII characters onto ASCII letters, which violates the exact-code-point contract |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #213 | 2026-10-24 | Initial feature design |
