# Design: Add greeting_letter_count library helper

**Issue**: #242
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/237-add-greeting-unique-char-count-library-helper/

## Overview

Follow the sibling count helpers. Call `greet(name)`, which validates the name, then count the characters in the completed greeting for which `str.isalpha()` is true. Export the helper from the package root and document it in the README Library section. No new import, module, or dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_unique_char_count`, separated from its neighbors by two blank lines:

```python
def greeting_letter_count(name: str) -> int:
    return sum(character.isalpha() for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Letter rule.** `str.isalpha()` is true for Unicode letters such as `ë` and false for digits, spaces, `,`, and `'`.
- **Return type.** `sum` over booleans returns a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_letter_count as greeting_letter_count` immediately after the `greeting_length` import line;
- add `"greeting_letter_count"` to `__all__` immediately after `"greeting_length"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_letter_count,` to the import list immediately after `greeting_length,`;
- add the example `greeting_letter_count("Ada")  # 8` immediately after `greeting_unique_char_count("Ada")  # 9`;
- add this exact prose line immediately after the `greeting_unique_char_count` prose line:

```markdown
`greeting_letter_count` counts the characters in the complete greeting (not the name alone) for which `str.isalpha()` is true, including the five letters of `Hello`; non-ASCII letters such as `ë` are counted, while digits, spaces, and punctuation are not, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_letter_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_letter_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_letter_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts `str.isalpha()` characters in `greet(name)`: `"Ada"` → `8`, `"Ada Lovelace"` → `16`, `"R2D2"` → `7`, `"Zoë"` → `8`, `"O'Brien"` → `11` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `sum(character.isalpha() for character in greet(name))` | Selected | Unicode-aware letter rule from the standard library; matches the one-line generator style of the sibling count helpers |
| ASCII ranges `A`–`Z` / `a`–`z` | Rejected | Would duplicate the uppercase and lowercase helpers and miss `ë`, which the issue requires |
| Normalize with `unicodedata.normalize` before counting | Rejected | The issue places normalization out of scope |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #242 | 2026-10-24 | Initial feature design |
