# Design: Add greeting_base85 library helper

**Issue**: #287
**Date**: 2026-10-26
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/263-add-greeting-base32-library-helper/

## Overview

Follow `greeting_base32` and `greeting_base64`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `base64.b85encode(...).decode("ascii")`. Export the helper from the package root and document it in the README Library section. `base64` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_base64` and before `greeting_rot13`, separated from its neighbors by two blank lines:

```python
def greeting_base85(name: str) -> str:
    return base64.b85encode(greet(name).encode("utf-8")).decode("ascii")
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `b85encode` (default `pad=False`) returns ASCII `bytes` in the RFC 1924 alphabet, with no padding, delimiters, or line breaks. `.decode("ascii")` turns that into a `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_base85 as greeting_base85` immediately after the `greeting_base64` import, before the `greeting_blake2b` import;
- add `"greeting_base85"` to `__all__` immediately after `"greeting_base64"`, before `"greeting_blake2b"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_base85,` to the import list immediately after `greeting_base64,`, before `greeting_blake2b,`;
- add the example `greeting_base85("Ada")  # "NM&qnZ!91|WMK"` immediately after the `greeting_base32("Ada")` example;
- add this exact prose line immediately after the `greeting_base32` prose line:

```markdown
`greeting_base85` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its Base85 encoding from `base64.b85encode` as a `str`, using the RFC 1924 alphabet with no padding, no `<~ ~>` delimiters, and no line breaks; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_base85_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_base85_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_base85(name: str) -> str` | Valid nonblank string name | RFC 1924 Base85 `str` without padding. Invalid input raises `ValueError("name must not be blank")` | Base85 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact results for `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `base64.b85encode(greet(name).encode("utf-8")).decode("ascii")` | Selected | Standard library; already imported; one-line style matches `greeting_base32`/`greeting_base64` |
| `base64.a85encode(...)` (Adobe Ascii85) | Rejected | Out of scope per issue |
| `base64.z85encode(...)` | Rejected | Out of scope; added only in Python 3.13, not available on 3.12 |
| `b85encode(..., pad=True)` | Rejected | Issue requires the default unpadded form |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #287 | 2026-10-26 | Initial feature design |
