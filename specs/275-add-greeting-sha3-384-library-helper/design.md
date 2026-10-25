# Design: Add greeting_sha3_384 library helper

**Issue**: #275
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/272-add-greeting-sha3-512-library-helper/

## Overview

Follow `greeting_sha3_256` and `greeting_sha3_512`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.sha3_384(...).hexdigest()`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_sha3_256` and before `greeting_sha3_512`, separated from its neighbors by two blank lines:

```python
def greeting_sha3_384(name: str) -> str:
    return hashlib.sha3_384(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 96-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_sha3_384 as greeting_sha3_384` immediately after the `greeting_sha3_256` import;
- add `"greeting_sha3_384"` to `__all__` immediately after `"greeting_sha3_256"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_sha3_384,` to the import list immediately after `greeting_sha3_256,`;
- add the example `greeting_sha3_384("Ada")  # "1a0e27fabec84a7b6ff60b8feb3cb3a8f6c3838c4242005c74f61de0149c524ac44e5f4d417d35726285bd9ee10b470b"` immediately after the `greeting_sha3_256("Ada")` example;
- add this exact prose line immediately after the `greeting_sha3_256` prose line:

```markdown
`greeting_sha3_384` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA3-384 digest from `hashlib.sha3_384` as 96 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_sha3_384_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_sha3_384_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_sha3_384(name: str) -> str` | Valid nonblank string name | 96-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | SHA3-384 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact digests of `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.sha3_384(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches the sibling SHA3 helpers |
| `hashlib.new("sha3_384", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| Reuse `greeting_sha384` | Rejected | SHA-384 (SHA-2) and SHA3-384 (Keccak) produce different digests |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #275 | 2026-10-25 | Initial feature design |
