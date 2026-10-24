# Design: Add greeting_space_count library helper

**Issue**: #230
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/227-add-greeting-digit-count-library-helper/

## Overview

Mirror `greeting_digit_count`. Call `greet(name)`, which validates the name, then count the U+0020 characters of the completed greeting. Export the helper from the package root and document it in the README Library section. No new module, constant, or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_digit_count`, separated from its neighbors by two blank lines:

```python
def greeting_space_count(name: str) -> int:
    return greet(name).count(" ")
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** `str.count(" ")` counts exactly the code point U+0020. Tab U+0009, newline U+000A, no-break space U+00A0, and other Unicode whitespace are not counted.
- **Return type.** `str.count` returns a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_space_count as greeting_space_count` immediately after the `greeting_sha256` import line;
- add `"greeting_space_count"` to `__all__` immediately after `"greeting_sha256"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_space_count,` to the import list immediately after `greeting_sha256,`;
- add the example `greeting_space_count("Ada Lovelace")  # 2` immediately after `greeting_digit_count("R2D2")  # 2`;
- add this exact prose line immediately after the `greeting_digit_count` prose line:

```markdown
`greeting_space_count` counts the ASCII space U+0020 in the complete greeting (not the name alone), including the space after `Hello,`; tabs, newlines, no-break spaces, and other Unicode whitespace are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_space_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_space_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_space_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts U+0020 in `greet(name)`: `"Ada"` → `1`, `"Ada Lovelace"` → `2`, `"Grace Brewster Hopper"` → `3`, `"Ada\tLovelace"` → `1`, `"Ada\nLovelace"` → `1`, `"Ada\u00a0Lovelace"` → `1` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greet(name).count(" ")` | Selected | Exact single-code-point contract; simplest standard-library expression |
| `sum(character == " " for character in greet(name))` | Rejected | Equivalent result with more code than `str.count` |
| `character.isspace()` | Rejected | Counts tabs, newlines, and no-break spaces, which the issue excludes |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #230 | 2026-10-24 | Initial feature design |
