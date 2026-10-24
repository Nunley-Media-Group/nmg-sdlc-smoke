# Design: Add greeting_lowercase_count library helper

**Issue**: #224
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/221-add-greeting-uppercase-count-library-helper/

## Overview

Mirror `greeting_uppercase_count`. Call `greet(name)`, which validates the name, then count the characters of the completed greeting that fall in the ASCII range `a`–`z`. Export the helper from the package root and document it in the README Library section. No new module, constant, or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_uppercase_count`, separated from its neighbors by two blank lines:

```python
def greeting_lowercase_count(name: str) -> int:
    return sum("a" <= character <= "z" for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** The code-point range check `"a" <= character <= "z"` counts exactly the 26 ASCII lowercase letters U+0061–U+007A. There is no case conversion and no Unicode normalization. Precomposed accented letters such as U+00E9 and fullwidth letters such as U+FF42 are not counted.
- **Return type.** `sum` over booleans starts at the `int` `0`, so the result is a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_lowercase_count as greeting_lowercase_count` immediately after the `greeting_length` import line;
- add `"greeting_lowercase_count"` to `__all__` immediately after `"greeting_length"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_lowercase_count,` to the import list immediately after `greeting_length,`;
- add the example `greeting_lowercase_count("Ada")  # 6` immediately after `greeting_uppercase_count("Ada")  # 2`;
- add this exact prose line immediately after the `greeting_uppercase_count` prose line:

```markdown
`greeting_lowercase_count` counts the 26 ASCII lowercase letters `a`–`z` in the complete greeting (not the name alone), including the `ello` in `Hello`; uppercase, accented, and fullwidth letters are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_lowercase_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_lowercase_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_lowercase_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts `a`–`z` code points in `greet(name)`: `"Ada"` → `6`, `"abc xyz"` → `10`, `"BOB 42!"` → `4`, `"é"` (U+00E9) → `4`, `"ｂｃ"` (U+FF42 U+FF43) → `4` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Code-point range check `"a" <= character <= "z"` | Selected | Exact 26-code-point contract; matches `greeting_uppercase_count` |
| `character.islower()` | Rejected | Counts accented and fullwidth lowercase letters, which the issue excludes |
| Membership in `string.ascii_lowercase` | Rejected | Equivalent result but adds an import; the range check matches the sibling's inline style |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #224 | 2026-10-24 | Initial feature design |
