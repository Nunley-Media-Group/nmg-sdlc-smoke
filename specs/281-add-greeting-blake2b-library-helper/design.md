# Design: Add greeting_blake2b library helper

**Issue**: #281
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/278-add-greeting-sha3-224-library-helper/

## Overview

Follow the existing digest helpers such as `greeting_sha3_224`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.blake2b(...).hexdigest()` with default parameters. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_sha3_512` and before `greeting_base32`, separated from its neighbors by two blank lines:

```python
def greeting_blake2b(name: str) -> str:
    return hashlib.blake2b(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Parameters.** BLAKE2b defaults: `digest_size=64`, with no `key`, `salt`, or `person`.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 128-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_blake2b as greeting_blake2b` immediately after the `greeting_base64` import and before the `greeting_bytes` import;
- add `"greeting_blake2b"` to `__all__` immediately after `"greeting_base64"` and before `"greeting_bytes"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_blake2b,` to the import list immediately after `greeting_base64,` and before `greeting_bytes,`;
- add the example `greeting_blake2b("Ada")  # "dacd0313406557f10115a4268fb435f4452c16872be1455fdf41b27fdcd3d1e6dba61210d8b48f846b7c23c68527c53c13bb10e794168d286a376d63513939d4"` immediately after the `greeting_sha3_512("Ada")` example;
- add this exact prose line immediately after the `greeting_sha3_512` prose line:

```markdown
`greeting_blake2b` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its BLAKE2b digest from `hashlib.blake2b` with default parameters (64-byte digest, no key, salt, or personalization) as 128 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_blake2b_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_blake2b_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_blake2b(name: str) -> str` | Valid nonblank string name | 128-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | Default-parameter BLAKE2b of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact digests of `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.blake2b(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches the sibling digest helpers |
| `hashlib.new("blake2b", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| `hashlib.blake2s` or a custom `digest_size` | Rejected | Out of scope; the issue specifies default-parameter BLAKE2b |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #281 | 2026-10-25 | Initial feature design |
