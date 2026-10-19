# Design: Add greeting_base64 library helper

**Issue**: #209
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing derived-value helper pattern (`greeting_bytes`, `greeting_sha256`):
1. Call `greet(name)`, which validates the name.
2. Encode the completed greeting as UTF-8.
3. Return the standard-library `base64.b64encode` result decoded to an ASCII `str`.

Export the helper from the package root and document it in the README Library section. No new module, constant, or runtime dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import base64` as the first line, immediately before `import hashlib`;
- add the following immediately after `greeting_sha256`, separated from its neighbors by two blank lines:

```python
def greeting_base64(name: str) -> str:
    return base64.b64encode(greet(name).encode("utf-8")).decode("ascii")
```

- **Validation.** `greet(name)` runs first. Invalid names therefore propagate its `ValueError("name must not be blank")` unchanged, and nothing is encoded.
- **Encoding.** `.encode("utf-8")` is the same call `greeting_bytes` and `greeting_sha256` make. It encodes the exact code points of the completed greeting with no stripping, case conversion, or Unicode normalization. Precomposed U+00EB and decomposed `e` + U+0308 therefore produce different bytes and different results.
- **Output.** `base64.b64encode` uses the RFC 4648 standard alphabet (`A`–`Z`, `a`–`z`, `0`–`9`, `+`, `/`), pads with `=`, and never inserts line breaks. `.decode("ascii")` turns its `bytes` result into a Python `str`. The function is pure and platform-independent.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_base64 as greeting_base64` immediately after `from .greet import greet, greet_many`;
- add `"greeting_base64"` to `__all__` immediately after `"greet_many"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_base64,` to the import list immediately after `greet_many,`;
- add the example `greeting_base64("Ada")  # "SGVsbG8sIEFkYQ=="` immediately after the `greeting_sha256("Ada")  # "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"` line, as the last line of the Python block;
- add this exact prose line immediately after the `greeting_sha256` prose line:

```markdown
`greeting_base64` encodes the complete greeting (not the name alone) as UTF-8 and returns its standard Base64 encoding as a `str`, using the RFC 4648 alphabet with `+` and `/`, `=` padding, and no line breaks; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- five independent acceptance scenarios go in `tests/features/add_greeting_base64_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_base64_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_base64(name: str) -> str` | Valid nonblank string name | Standard-alphabet, `=`-padded, unwrapped Base64 `str`. Invalid input raises `ValueError("name must not be blank")` | Base64 of `greet(name).encode("utf-8")`: `"Ada"` → `SGVsbG8sIEFkYQ==`; `"a?>"` → `SGVsbG8sIGE/Pg==`; `"a>>"` → `SGVsbG8sIGE+Pg==`; `"Bo"` → `SGVsbG8sIEJv`; `"Bob~"` → `SGVsbG8sIEJvYn4=`; `"Zo\u00eb"` → `SGVsbG8sIFpvw6s=`; `"Zoe\u0308"` → `SGVsbG8sIFpvZcyI` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `base64.b64encode(...).decode("ascii")` over the UTF-8 encoding of `greet(name)` | Selected | Standard library only; standard alphabet with `=` padding; no line breaks; returns `str` |
| `base64.encodebytes` or `binascii.b2a_base64` | Rejected | Both append a trailing newline, and `encodebytes` wraps output at 76 characters; the issue requires no line breaks |
| `base64.urlsafe_b64encode` or stripping `=` padding | Rejected | The issue requires the standard `+`/`/` alphabet with `=` padding |
| Return the raw `bytes` from `b64encode` | Rejected | The issue requires a `str` |
| Unicode NFC/NFD normalization before encoding | Rejected | The issue requires exact code points; precomposed and decomposed names must produce different results |
| `nmg-smoke --base64` flag | Rejected | The issue limits the change to the library; CLI output stays unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #209 | 2026-10-18 | Initial feature design |
