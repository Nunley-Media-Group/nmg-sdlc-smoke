# Design: Add greeting_punctuation_count library helper

**Issue**: #233
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/230-add-greeting-space-count-library-helper/

## Overview

Mirror the sibling count helpers. Call `greet(name)`, which validates the name, then count the characters of the completed greeting that belong to `string.punctuation`. Export the helper from the package root and document it in the README Library section. The only new import is the standard-library `string` module; no new module or dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import string` to the standard-library import block, keeping Ruff's import order (after `import hashlib`);
- add the following immediately after `greeting_space_count`, separated from its neighbors by two blank lines:

```python
def greeting_punctuation_count(name: str) -> int:
    return sum(character in string.punctuation for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Matching.** Membership in `string.punctuation` matches exactly the 32 ASCII punctuation characters. Letters, digits, whitespace, and non-ASCII characters such as U+FF01, U+2019, and U+3001 are not members.
- **Return type.** `sum` over booleans returns a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_punctuation_count as greeting_punctuation_count` immediately after the `greeting_lowercase_count` import line;
- add `"greeting_punctuation_count"` to `__all__` immediately after `"greeting_lowercase_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_punctuation_count,` to the import list immediately after `greeting_lowercase_count,`;
- add the example `greeting_punctuation_count("O'Brien")  # 2` immediately after `greeting_space_count("Ada Lovelace")  # 2`;
- add this exact prose line immediately after the `greeting_space_count` prose line:

```markdown
`greeting_punctuation_count` counts the 32 ASCII punctuation characters in Python's `string.punctuation` in the complete greeting (not the name alone), including the comma after `Hello`; non-ASCII punctuation and look-alikes such as `！`, `’`, and `、` are not counted, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_punctuation_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_punctuation_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_punctuation_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts `string.punctuation` characters in `greet(name)`: `"Ada"` → `1`, `"O'Brien"` → `2`, `"Ada!?"` → `3`, `"a.b-c_d"` → `4`, `"Ada！"` → `1`, `"O’Brien"` → `1`, `"Ada、"` → `1`, `"Ada Lovelace 42"` → `1` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `sum(character in string.punctuation for character in greet(name))` | Selected | Exact ASCII set from the standard library; matches the sibling count-helper style |
| `unicodedata.category(character).startswith("P")` | Rejected | Counts non-ASCII punctuation and excludes ASCII symbols such as `$`, `+`, and `^`, which the issue includes |
| A hand-written punctuation literal | Rejected | Duplicates `string.punctuation` and risks drift |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #233 | 2026-10-24 | Initial feature design |
