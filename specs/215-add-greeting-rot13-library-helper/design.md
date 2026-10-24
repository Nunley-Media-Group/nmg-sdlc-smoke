# Design: Add greeting_rot13 library helper

**Issue**: #215
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing transformed-greeting helper pattern (`greeting_reversed`, `greeting_casefold`, `greeting_base64`):
1. Call `greet(name)`, which validates the name.
2. Return the standard-library `codecs.encode(..., "rot13")` result of the completed greeting.

Export the helper from the package root and document it in the README Library section. No new module, constant, or runtime dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import codecs` immediately after `import base64` (keeping imports sorted for Ruff);
- add the following immediately after `greeting_base64`, separated from its neighbors by two blank lines:

```python
def greeting_rot13(name: str) -> str:
    return codecs.encode(greet(name), "rot13")
```

- **Validation.** `greet(name)` runs first. Invalid names therefore propagate its `ValueError("name must not be blank")` unchanged.
- **Rotation.** The `rot13` text codec maps only `A`–`Z` and `a`–`z`, each 13 places within its case. Every other code point—punctuation, spaces, digits, accented letters such as `ë`, and fullwidth letters such as `Ｚ`—passes through unchanged. It returns a `str`, is pure, and is its own inverse.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_rot13 as greeting_rot13` immediately after `from .greet import greeting_reversed as greeting_reversed`;
- add `"greeting_rot13"` to `__all__` immediately after `"greeting_reversed"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_rot13,` to the import list immediately after `greeting_reversed,`;
- add the example `greeting_rot13("Ada")  # "Uryyb, Nqn"` as the last line of the first Python block;
- add this exact prose line immediately after the `greeting_base64` prose line:

```markdown
`greeting_rot13` applies ROT13 to the complete greeting (not the name alone), rotating only the ASCII letters `A`–`Z` and `a`–`z` by 13 places within their case and leaving every other character, including non-ASCII letters, unchanged; applying ROT13 again restores the greeting, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- five independent acceptance scenarios go in `tests/features/add_greeting_rot13_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_rot13_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_rot13(name: str) -> str` | Valid nonblank string name | ROT13 `str` of the completed greeting. Invalid input raises `ValueError("name must not be blank")` | `"Ada"` → `Uryyb, Nqn`; `"Mary-Jane O'Neil"` → `Uryyb, Znel-Wnar B'Arvy`; `"Zoë"` → `Uryyb, Mbë`; `"Ｚed 42"` → `Uryyb, Ｚrq 42` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `codecs.encode(greet(name), "rot13")` | Selected | Standard library; ASCII-only; returns `str`; one line |
| `str.translate` with a `str.maketrans` table | Rejected | Equivalent behavior but needs a module-level table constant |
| Rotating via `str.isalpha()` | Rejected | Would rotate or mishandle non-ASCII letters such as `ë` and `Ｚ` |
| `nmg-smoke --rot13` flag | Rejected | The issue limits the change to the library; CLI output stays unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #215 | 2026-10-24 | Initial feature design |
