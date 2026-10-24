# Design: Add greeting_digit_count library helper

**Issue**: #227
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/224-add-greeting-lowercase-count-library-helper/

## Overview

Mirror `greeting_lowercase_count`. Call `greet(name)`, which validates the name, then count the characters of the completed greeting that fall in the ASCII range `0`–`9`. Export the helper from the package root and document it in the README Library section. No new module, constant, or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_lowercase_count`, separated from its neighbors by two blank lines:

```python
def greeting_digit_count(name: str) -> int:
    return sum("0" <= character <= "9" for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** The code-point range check `"0" <= character <= "9"` counts exactly the ten ASCII digits U+0030–U+0039. Fullwidth digits such as U+FF11, Arabic-Indic digits such as U+0663, and superscripts such as U+00B2 are not counted.
- **Return type.** `sum` over booleans starts at the `int` `0`, so the result is a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_digit_count as greeting_digit_count` immediately after the `greeting_casefold` import line;
- add `"greeting_digit_count"` to `__all__` immediately after `"greeting_casefold"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_digit_count,` to the import list immediately after `greeting_casefold,`;
- add the example `greeting_digit_count("R2D2")  # 2` immediately after `greeting_lowercase_count("Ada")  # 6`;
- add this exact prose line immediately after the `greeting_lowercase_count` prose line:

```markdown
`greeting_digit_count` counts the ten ASCII digits `0`–`9` in the complete greeting (not the name alone); fullwidth, other-script, and superscript digits are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_digit_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_digit_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_digit_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts `0`–`9` code points in `greet(name)`: `"R2D2"` → `2`, `"Agent 007"` → `3`, `"Ada"` → `0`, `"１２"` (U+FF11 U+FF12) → `0`, `"٣"` (U+0663) → `0`, `"x²"` (U+00B2) → `0` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Code-point range check `"0" <= character <= "9"` | Selected | Exact ten-code-point contract; matches `greeting_lowercase_count` |
| `character.isdigit()` / `character.isdecimal()` | Rejected | Counts fullwidth, Arabic-Indic, and superscript digits, which the issue excludes |
| Membership in `string.digits` | Rejected | Equivalent result but adds an import; the range check matches the siblings' inline style |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #227 | 2026-10-24 | Initial feature design |
