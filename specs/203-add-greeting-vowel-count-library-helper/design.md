# Design: Add greeting_vowel_count library helper

**Issue**: #203
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing derived-number helper pattern (`greeting_length`, `greeting_word_count`). Call `greet(name)`, which validates the name, then count the characters of the completed greeting that belong to the ten ASCII vowels. Export the helper from the package root and document it in the README Library section. No new module, constant, or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_word_count`, separated from its neighbors by two blank lines:

```python
def greeting_vowel_count(name: str) -> int:
    return sum(character in "aeiouAEIOU" for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** The check compares each single code point of the Python `str` against exactly `aeiouAEIOU`. There is no case conversion and no Unicode normalization.
  - `y`/`Y`, precomposed accented letters such as U+00C9, and fullwidth letters such as U+FF21 and U+FF41 are not counted.
  - A decomposed `E` followed by U+0301 counts its base `E` only.
- **Return type.** `sum` over booleans starts at the `int` `0`, so the result is a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_vowel_count as greeting_vowel_count` immediately after the `greeting_starts_with_hello` import line;
- add `"greeting_vowel_count"` to `__all__` immediately after `"greeting_starts_with_hello"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_vowel_count,` to the import list immediately after `greeting_starts_with_hello,`;
- add the example `greeting_vowel_count("Ada")  # 4` immediately after `greeting_word_count("Ada Lovelace")  # 3`, as the last line of the Python block;
- add this exact prose line immediately after the `greeting_word_count` prose line:

```markdown
`greeting_vowel_count` counts the ten ASCII vowels `a e i o u A E I O U` in the complete greeting (not the name alone); `y`, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_vowel_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_vowel_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_vowel_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts `aeiouAEIOU` code points in `greet(name)`: `"Ada"` → `4`, `"AEIOU aeiou"` → `12`, `"Bcd"` → `2`, `"Ady"` → `3`, `"Émile"` (U+00C9) → `4`, `"Ａｄａ"` (U+FF21 U+FF44 U+FF41) → `2` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Membership test against the literal `"aeiouAEIOU"` | Selected | Exact ten-code-point contract; standard library only; no case conversion |
| `casefold()`/`lower()` before matching against `"aeiou"` | Rejected | Case conversion can map non-ASCII characters onto ASCII vowels, which violates the exact-code-point contract |
| Unicode normalization (NFD) to count accented base letters | Rejected | The issue excludes accented vowels and normalization |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #203 | 2026-10-18 | Initial feature design |
