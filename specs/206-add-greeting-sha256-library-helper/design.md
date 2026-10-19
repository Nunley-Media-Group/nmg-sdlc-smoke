# Design: Add greeting_sha256 library helper

**Issue**: #206
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing derived-value helper pattern (`greeting_bytes`, `greeting_reversed`). Call `greet(name)`, which validates the name. Then encode the completed greeting as UTF-8 and return the standard-library `hashlib.sha256` hex digest. Export the helper from the package root and document it in the README Library section. No new module, constant, or runtime dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import hashlib` as the first line, immediately before `from collections.abc import Iterable`;
- add the following immediately after `greeting_vowel_count`, separated from its neighbors by two blank lines:

```python
def greeting_sha256(name: str) -> str:
    return hashlib.sha256(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged, and no digest is computed.
- **Encoding.** `.encode("utf-8")` is the same call `greeting_bytes` makes. The exact code points of the completed greeting are encoded, with no stripping, case conversion, or Unicode normalization. Precomposed U+00EB and decomposed `e` + U+0308 therefore produce different byte sequences and different digests.
- **Output.** `hexdigest()` returns a Python `str` of exactly 64 lowercase hexadecimal characters. `hashlib.sha256` is always available in CPython, so the result is identical on every platform.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_sha256 as greeting_sha256` immediately after the `greeting_reversed` import line;
- add `"greeting_sha256"` to `__all__` immediately after `"greeting_reversed"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_sha256,` to the import list immediately after `greeting_reversed,`;
- add the example `greeting_sha256("Ada")  # "7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66"` immediately after `greeting_vowel_count("Ada")  # 4`, as the last line of the Python block;
- add this exact prose line immediately after the `greeting_vowel_count` prose line:

```markdown
`greeting_sha256` encodes the complete greeting (not the name alone) as UTF-8 and returns its SHA-256 digest as 64 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_sha256_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_sha256_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_sha256(name: str) -> str` | Valid nonblank string name | 64-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | SHA-256 of `greet(name).encode("utf-8")`: `"Ada"` → `7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66`; `"Zo\u00eb"` → `aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524`; `"Zoe\u0308"` → `af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.sha256(...).hexdigest()` over the UTF-8 encoding of `greet(name)` | Selected | Standard library only; lowercase 64-character hex `str`; platform-independent |
| Unicode NFC/NFD normalization before hashing | Rejected | The issue requires exact code points; precomposed and decomposed names must produce different digests |
| Return the raw `bytes` digest from `digest()` | Rejected | The issue requires a 64-character lowercase hexadecimal `str` |
| `nmg-smoke --sha256` flag | Rejected | The issue limits the change to the library; CLI output stays unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #206 | 2026-10-18 | Initial feature design |
