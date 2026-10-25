# Design: Add greeting_adler32 library helper

**Issue**: #248
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/245-add-greeting-crc32-library-helper/

## Overview

Follow `greeting_crc32`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `zlib.adler32` of the bytes. Export the helper from the package root and document it in the README Library section. `zlib` is already imported in `greet.py`, so no new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_crc32`, separated from its neighbors by two blank lines:

```python
def greeting_adler32(name: str) -> int:
    return zlib.adler32(greet(name).encode("utf-8"))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** On Python 3, `zlib.adler32` returns an unsigned `int` in `0`–`4294967295`. The function does not pass a starting value.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_adler32 as greeting_adler32` immediately after the `from .greet import greet, greet_many` line;
- add `"greeting_adler32"` to `__all__` immediately after `"greet_many"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_adler32,` to the import list immediately after `greet_many,`;
- add the example `greeting_adler32("Ada")  # 312279879` immediately after `greeting_crc32("Ada")  # 2761732226`;
- add this exact prose line immediately after the `greeting_crc32` prose line:

```markdown
`greeting_adler32` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its unsigned Adler-32 checksum from `zlib.adler32` as an `int` between `0` and `4294967295`; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different checksums, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_adler32_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_adler32_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_adler32(name: str) -> int` | Valid nonblank string name | Unsigned `int` checksum. Invalid input raises `ValueError("name must not be blank")` | Adler-32 of the UTF-8 bytes of `greet(name)`: `"Ada"` → `312279879`, `"Ada Lovelace"` → `1063257746`, `"Zoë"` → `400032888` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `zlib.adler32(greet(name).encode("utf-8"))` | Selected | Standard library; already imported; one-line style matches `greeting_crc32` |
| Hand-rolled Adler-32 loop | Rejected | Duplicates the standard library and adds code to test |
| Return an 8-character hex string | Rejected | The issue requires an `int` and puts hex output out of scope |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #248 | 2026-10-25 | Initial feature design |
