# Design: Add public greeting_reversed library helper

**Issue**: #200
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing derived-string helper pattern (`greeting_casefold`). Call `greet(name)`, which validates the name, then return its code-point reversal. Export the helper from the package root and document it in the README Library section. No new module or dependency is needed.

## Architecture

Add the following to `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_casefold`, separated by two blank lines:

```python
def greeting_reversed(name: str) -> str:
    return greet(name)[::-1]
```

Calling `greet` first means invalid names raise `greet`'s `ValueError("name must not be blank")` unchanged, so no greeting is produced. Slicing with step `-1` reverses the Python `str` by code point, with no Unicode normalization or grapheme clustering. A precomposed `ë` (U+00EB) therefore stays a single character, while a combining mark moves to the other side of its base character.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_reversed as greeting_reversed` immediately after the `greeting_length` import line;
- add `"greeting_reversed"` to `__all__` immediately after `"greeting_length"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_reversed,` to the import list immediately after `greeting_length,`;
- add the example `greeting_reversed("Ada")  # "adA ,olleH"` immediately after `greeting_casefold("Straße")  # "hello, strasse"`;
- add this prose line immediately after the `greeting_casefold` prose line: `` `greeting_reversed` reverses the complete greeting by Unicode code point (not by grapheme cluster) and uses the same validation as `greet`; it does not change `greet` or CLI output. ``

Unit tests go in `tests/test_greet.py`. Three independent acceptance scenarios go in `tests/features/add_public_greeting_reversed_library_helper.feature`, with steps in `tests/features/steps/test_greeting_reversed_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_reversed(name: str) -> str` | Valid nonblank string name | Reversed greeting string; invalid input raises `ValueError("name must not be blank")` | Returns `greet(name)[::-1]`: `"Ada"` → `"adA ,olleH"`, `"Zoë"` (U+00EB) → `"ëoZ ,olleH"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greet(name)[::-1]` code-point reversal | Selected | Matches the issue's code-point contract; standard library only |
| Grapheme-cluster reversal | Rejected | Needs a third-party segmentation dependency; the project keeps zero runtime dependencies |
| `nmg-smoke --reverse` flag | Rejected | The issue limits the change to the library; CLI output stays unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #200 | 2026-10-06 | Initial feature design |
