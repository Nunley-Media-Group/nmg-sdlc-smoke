# Design: Add greeting_unique_char_count library helper

**Issue**: #237
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/233-add-greeting-punctuation-count-library-helper/

## Overview

Mirror the sibling count helpers. Call `greet(name)`, which validates the name, then return the size of the set of characters in the completed greeting. Export the helper from the package root and document it in the README Library section. No new import, module, or dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_punctuation_count`, separated from its neighbors by two blank lines:

```python
def greeting_unique_char_count(name: str) -> int:
    return len(set(greet(name)))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Distinctness.** A Python `set` of a `str` holds one entry per distinct code point, so the count is case-sensitive and unnormalized.
- **Return type.** `len` returns a Python `int`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_unique_char_count as greeting_unique_char_count` immediately after the `greeting_starts_with_hello` import line;
- add `"greeting_unique_char_count"` to `__all__` immediately after `"greeting_starts_with_hello"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_unique_char_count,` to the import list immediately after `greeting_starts_with_hello,`;
- add the example `greeting_unique_char_count("Ada")  # 9` immediately after `greeting_punctuation_count("O'Brien")  # 2`;
- add this exact prose line immediately after the `greeting_punctuation_count` prose line:

```markdown
`greeting_unique_char_count` counts the distinct Unicode code points in the complete greeting (not the name alone), including the characters of `Hello, `; the count is case-sensitive and applies no Unicode normalization, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_unique_char_count_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_unique_char_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_unique_char_count(name: str) -> int` | Valid nonblank string name | `int` count. Invalid input raises `ValueError("name must not be blank")` | Counts distinct code points in `greet(name)`: `"Ada"` → `9`, `"Bob"` → `8`, `"Ada Lovelace"` → `12`, `"ADA"` → `8`, `"Zoë"` → `8` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `len(set(greet(name)))` | Selected | Exact code-point distinctness with the standard library; matches the one-line sibling helper style |
| Normalize with `unicodedata.normalize` before counting | Rejected | The issue places normalization out of scope |
| `len(collections.Counter(greet(name)))` | Rejected | Adds an import for the same result |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #237 | 2026-10-24 | Initial feature design |
