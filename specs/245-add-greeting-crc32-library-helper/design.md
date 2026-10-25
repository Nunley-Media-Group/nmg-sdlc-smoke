# Design: Add greeting_crc32 library helper

**Issue**: #245
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/206-add-greeting-sha256-library-helper/

## Overview

Follow the sibling digest helpers. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `zlib.crc32` of the bytes. Export the helper from the package root and document it in the README Library section. The only new import is the standard-library `zlib` module. No new module or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import zlib` immediately after `import string`;
- add the following immediately after `greeting_url_encoded`, separated from its neighbors by two blank lines:

```python
def greeting_crc32(name: str) -> int:
    return zlib.crc32(greet(name).encode("utf-8"))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** On Python 3, `zlib.crc32` returns an unsigned `int` in `0`–`4294967295`. The function does not pass a starting value.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_crc32 as greeting_crc32` immediately after the `greeting_casefold` import line;
- add `"greeting_crc32"` to `__all__` immediately after `"greeting_casefold"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_crc32,` to the import list immediately after `greeting_casefold,`;
- add the example `greeting_crc32("Ada")  # 2761732226` immediately after `greeting_rot13("Ada")  # "Uryyb, Nqn"`;
- add this exact prose line immediately after the `greeting_url_encoded` prose line:

```markdown
`greeting_crc32` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its unsigned CRC-32 checksum from `zlib.crc32` as an `int` between `0` and `4294967295`; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different checksums, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_crc32_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_crc32_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_crc32(name: str) -> int` | Valid nonblank string name | Unsigned `int` checksum. Invalid input raises `ValueError("name must not be blank")` | CRC-32 of the UTF-8 bytes of `greet(name)`: `"Ada"` → `2761732226`, `"Ada Lovelace"` → `2495651459`, `"Zoë"` → `2271742533` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `zlib.crc32(greet(name).encode("utf-8"))` | Selected | Standard library; the one-line style matches `greeting_sha256` |
| `binascii.crc32` | Rejected | Gives the same result, but `zlib` is the conventional CRC-32 entry point; one module is enough |
| Return an 8-character hex string | Rejected | The issue requires an `int` and puts hex output out of scope |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #245 | 2026-10-25 | Initial feature design |
