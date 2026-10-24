# Design: Add greeting_uppercase_count library helper

**Issue**: #221
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/203-add-greeting-vowel-count-library-helper/

## Overview

Follow the derived-count helper pattern of `greeting_vowel_count`. Call `greet(name)`, which validates the name, then count the characters of the completed greeting that fall in the ASCII range `A`–`Z`. Export the helper from the package root and document it in the README Library section. No new module, constant, or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_vowel_count`, separated from its neighbors by two blank lines:

```python
def greeting_uppercase_count(name: str) -> int:
    return sum("A" <= character <= "Z" for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** The code-point range check `"A" <= character <= "Z"` counts exactly the 26 ASCII capitals U+0041–U+005A. There is no case conversion and no Unicode normalization. Precomposed accented capitals such as U+00C9 and fullwidth capitals such as U+FF22 are not counted.
- **Return type.** `sum` over booleans starts at the `int` `0`, so the result is a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_uppercase_count as greeting_uppercase_count` immediately after the `greeting_starts_with_hello` import line;
- add `"greeting_uppercase_count"` to `__all__` immediately after `"greeting_starts_with_hello"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_uppercase_count,` to the import list immediately after `greeting_starts_with_hello,`;
- add the example `greeting_uppercase_count("Ada")  # 2` immediately after `greeting_vowel_count("Ada")  # 4`;
- add this exact prose line immediately after the `greeting_vowel_count` prose line:

```markdown
`greeting_uppercase_count` counts the 26 ASCII capitals `A`–`Z` in the complete greeting (not the name alone), including the `H` in `Hello`; lowercase, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_uppercase_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_uppercase_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_uppercase_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts `A`–`Z` code points in `greet(name)`: `"Ada"` → `2`, `"ABC XYZ"` → `7`, `"bob 42!"` → `1`, `"Émile"` (U+00C9) → `1`, `"ＢＣ"` (U+FF22 U+FF23) → `1` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Code-point range check `"A" <= character <= "Z"` | Selected | Exact 26-code-point contract; standard library only |
| `character.isupper()` | Rejected | Counts accented and fullwidth capitals, which the issue excludes |
| Membership in `string.ascii_uppercase` | Rejected | Equivalent result but adds an import; the range check matches the sibling helpers' inline style |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #221 | 2026-10-24 | Initial feature design |
