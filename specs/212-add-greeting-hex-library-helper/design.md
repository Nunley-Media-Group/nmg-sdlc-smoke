# Design: Add greeting_hex library helper

**Issue**: #212
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/209-add-greeting-base64-library-helper/

## Overview

Follow the existing derived-value helper pattern (`greeting_bytes`, `greeting_sha256`, `greeting_base64`):
1. Call `greet(name)`, which validates the name.
2. Encode the completed greeting as UTF-8.
3. Return the built-in `bytes.hex()` result.

Export the helper from the package root and document it in the README Library section. No new module, import, constant, or runtime dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_base64`, separated from its neighbors by two blank lines:

```python
def greeting_hex(name: str) -> str:
    return greet(name).encode("utf-8").hex()
```

- **Validation.** `greet(name)` runs first. Invalid names therefore propagate its `ValueError("name must not be blank")` unchanged, and nothing is encoded.
- **Encoding.** `.encode("utf-8")` is the same call the sibling helpers make. It encodes the exact code points of the completed greeting with no stripping, case conversion, or Unicode normalization. Precomposed U+00EB and decomposed `e` + U+0308 therefore produce different bytes and different results.
- **Output.** `bytes.hex()` with no arguments returns a `str` of lowercase `0`–`9`/`a`–`f`, two characters per byte, with no separator and no `0x` prefix. The function is pure and platform-independent.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_hex as greeting_hex` immediately after `from .greet import greeting_has_underscore as greeting_has_underscore`;
- add `"greeting_hex"` to `__all__` immediately after `"greeting_has_underscore"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_hex,` to the import list immediately after `greeting_has_underscore,`;
- add the example `greeting_hex("Ada")  # "48656c6c6f2c20416461"` immediately after the `greeting_base64("Ada")  # "SGVsbG8sIEFkYQ=="` line, as the last line of the Python block;
- add this exact prose line immediately after the `greeting_base64` prose line:

```markdown
`greeting_hex` encodes the complete greeting (not the name alone) as UTF-8 and returns those bytes as a lowercase hexadecimal `str`, two characters per byte with no separators or `0x` prefix; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_hex_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_hex_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_hex(name: str) -> str` | Valid nonblank string name | Lowercase, unseparated, unprefixed hex `str`. Invalid input raises `ValueError("name must not be blank")` | `greet(name).encode("utf-8").hex()`: `"Ada"` → `48656c6c6f2c20416461`; `"Zoë"` → `48656c6c6f2c205a6fc3ab`; `"Zoë"` → `48656c6c6f2c205a6f65cc88`; `"é中"` → `48656c6c6f2c20c3a9e4b8ad` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `bytes.hex()` over the UTF-8 encoding of `greet(name)` | Selected | Built in; lowercase; no separator or prefix; returns `str`; no import needed |
| `binascii.hexlify(...).decode("ascii")` | Rejected | Same output but adds an import and a decode step for no benefit |
| `bytes.hex(sep)` or `.upper()` | Rejected | The issue requires lowercase output with no separators |
| Unicode NFC/NFD normalization before encoding | Rejected | The issue requires exact code points; precomposed and decomposed names must produce different results |
| `nmg-smoke --hex` flag | Rejected | The issue limits the change to the library; CLI output stays unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #212 | 2026-10-24 | Initial feature design |
