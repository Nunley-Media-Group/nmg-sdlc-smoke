# Design: Add greeting_base32 library helper

**Issue**: #263
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/209-add-greeting-base64-library-helper/

## Overview

Follow `greeting_base64`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `base64.b32encode(...).decode("ascii")`. Export the helper from the package root and document it in the README Library section. `base64` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately before `greeting_base64`, separated from its neighbors by two blank lines:

```python
def greeting_base32(name: str) -> str:
    return base64.b32encode(greet(name).encode("utf-8")).decode("ascii")
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `b32encode` returns ASCII `bytes` in the RFC 4648 alphabet with `=` padding and no line breaks; `.decode("ascii")` returns a `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_base32 as greeting_base32` immediately after the `greeting_adler32` import, before the `greeting_base64` import;
- add `"greeting_base32"` to `__all__` immediately after `"greeting_adler32"`, before `"greeting_base64"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_base32,` to the import list immediately after `greeting_adler32,`, before `greeting_base64,`;
- add the example `greeting_base32("Ada")  # "JBSWY3DPFQQECZDB"` immediately after the `greeting_base64("Ada")` example;
- add this exact prose line immediately after the `greeting_base64` prose line:

```markdown
`greeting_base32` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its standard Base32 encoding from `base64.b32encode` as a `str`, using the RFC 4648 alphabet of uppercase `A`–`Z` and `2`–`7`, `=` padding, and no line breaks; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_base32_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_base32_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_base32(name: str) -> str` | Valid nonblank string name | RFC 4648 Base32 `str` with `=` padding. Invalid input raises `ValueError("name must not be blank")` | Base32 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact results for `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `base64.b32encode(greet(name).encode("utf-8")).decode("ascii")` | Selected | Standard library; already imported; one-line style matches `greeting_base64` |
| `base64.b32hexencode(...)` | Rejected | Extended hex alphabet is out of scope |
| Strip `=` padding or lowercase the output | Rejected | The issue requires the standard padded uppercase form |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #263 | 2026-10-25 | Initial feature design |
