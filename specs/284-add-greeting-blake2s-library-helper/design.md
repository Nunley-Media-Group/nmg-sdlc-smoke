# Design: Add greeting_blake2s library helper

**Issue**: #284
**Date**: 2026-10-26
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/281-add-greeting-blake2b-library-helper/

## Overview

Follow the existing digest helpers such as `greeting_blake2b`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.blake2s(...).hexdigest()` with default parameters. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_blake2b` and before `greeting_base32`, separated from its neighbors by two blank lines:

```python
def greeting_blake2s(name: str) -> str:
    return hashlib.blake2s(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Parameters.** BLAKE2s defaults: `digest_size=32`, with no `key`, `salt`, or `person`.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 64-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_blake2s as greeting_blake2s` immediately after the `greeting_blake2b` import and before the `greeting_bytes` import;
- add `"greeting_blake2s"` to `__all__` immediately after `"greeting_blake2b"` and before `"greeting_bytes"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_blake2s,` to the import list immediately after `greeting_blake2b,` and before `greeting_bytes,`;
- add the example `greeting_blake2s("Ada")  # "68d52139de7dbb117ec790dad9989297d2dc4914ebd9b4d177d0e5da344edb14"` immediately after the `greeting_blake2b("Ada")` example;
- add this exact prose line immediately after the `greeting_blake2b` prose line:

```markdown
`greeting_blake2s` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its BLAKE2s digest from `hashlib.blake2s` with default parameters (32-byte digest, no key, salt, or personalization) as 64 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_blake2s_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_blake2s_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_blake2s(name: str) -> str` | Valid nonblank string name | 64-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | Default-parameter BLAKE2s of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact digests of `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.blake2s(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches the sibling digest helpers |
| `hashlib.new("blake2s", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| `hashlib.blake2b(..., digest_size=32)` | Rejected | A different algorithm with different output; the issue specifies default-parameter BLAKE2s |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #284 | 2026-10-26 | Initial feature design |
