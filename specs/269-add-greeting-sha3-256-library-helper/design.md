# Design: Add greeting_sha3_256 library helper

**Issue**: #269
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/266-add-greeting-sha224-library-helper/

## Overview

Follow `greeting_sha224`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.sha3_256(...).hexdigest()`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_sha224`, separated from its neighbors by two blank lines:

```python
def greeting_sha3_256(name: str) -> str:
    return hashlib.sha3_256(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 64-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_sha3_256 as greeting_sha3_256` immediately after the `greeting_sha384` import, before the `greeting_sha512` import (ASCII order);
- add `"greeting_sha3_256"` to `__all__` immediately after `"greeting_sha384"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_sha3_256,` to the import list immediately after `greeting_sha384,`;
- add the example `greeting_sha3_256("Ada")  # "8fe4a55d0487c2a730a2f841a99b44d01ca1f235c30ab3a452af08ca7cd531d4"` immediately after the `greeting_sha224("Ada")` example;
- add this exact prose line immediately after the `greeting_sha224` prose line:

```markdown
`greeting_sha3_256` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA3-256 digest from `hashlib.sha3_256` as 64 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_sha3_256_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_sha3_256_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_sha3_256(name: str) -> str` | Valid nonblank string name | 64-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | SHA3-256 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact digests of `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.sha3_256(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches the SHA-2 helpers |
| `hashlib.new("sha3_256", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| Reuse `greeting_sha256` | Rejected | SHA-256 (SHA-2) and SHA3-256 (Keccak) produce different digests |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #269 | 2026-10-25 | Initial feature design |
