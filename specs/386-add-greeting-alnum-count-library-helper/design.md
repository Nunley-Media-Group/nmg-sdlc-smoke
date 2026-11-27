# Design: Add greeting_alnum_count library helper

**Issue**: #386
**Date**: 2026-11-27
**Status**: Approved
**Author**: NMG

## Overview

Count the `str.isalnum()` code points in the existing `greet(name)` result, export the helper from the package root, and document it in the README Library section. The change adds no import, module, or runtime dependency, and the CLI stays unchanged.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_letter_count` and before `greeting_non_ascii_count`, with the same two-blank-line spacing as the functions around it:

```python
def greeting_alnum_count(name: str) -> int:
    return sum(character.isalnum() for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names raise its `ValueError("name must not be blank")` unchanged.
- **Counting rule.** Iterating a Python `str` yields code points. `str.isalnum()` is true for letters and for Unicode decimal, digit, and numeric characters, such as U+0663. It is false for spaces, punctuation, combining marks such as U+0308, and emoji. No normalization is applied, and `sum` over booleans returns an `int`.

In `src/nmg_sdlc_smoke/__init__.py`, follow the existing alphabetical order (`greeting_adler32` < `greeting_alnum_count` < `greeting_ascii85`):

- add `from .greet import greeting_alnum_count as greeting_alnum_count` immediately after the `greeting_adler32` import;
- add `"greeting_alnum_count"` to `__all__` immediately after `"greeting_adler32"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_alnum_count,` to the import list immediately after `greeting_adler32,`;
- add the example `greeting_alnum_count("R2-D2")  # 9` immediately after the `greeting_letter_count("Ada")  # 8` example;
- add this exact prose line immediately after the `greeting_letter_count` prose line:

```markdown
`greeting_alnum_count` counts the characters in the complete greeting (not the name alone) for which `str.isalnum()` is true, including the five letters of `Hello`, so `Ada` gives `8` and `R2-D2` gives `9`; non-ASCII letters such as `ë` and Unicode digits such as U+0663 are counted, while spaces, punctuation, combining marks, and emoji are not, no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: four independent acceptance scenarios go in `tests/features/add_greeting_alnum_count_library_helper.feature`, with steps in `tests/features/steps/test_greeting_alnum_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_alnum_count(name: str) -> int` | Valid nonblank string name | Count of code points in `greet(name)` for which `str.isalnum()` is true. Invalid input raises `ValueError("name must not be blank")` | See AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `sum(c.isalnum() for c in greet(name))` | Selected | Mirrors `greeting_letter_count`; reuses validation |
| `greeting_letter_count(name) + greeting_digit_count(name)` | Rejected | Misses non-ASCII digits and builds the greeting twice |
| `isalpha() or isdecimal()` per character | Rejected | Narrower than the documented `str.isalnum()` rule |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #386 | 2026-11-27 | Initial feature design |
