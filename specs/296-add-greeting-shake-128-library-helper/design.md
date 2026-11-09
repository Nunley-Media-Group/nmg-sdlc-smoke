# Design: Add greeting_shake_128 library helper

**Issue**: #296
**Date**: 2026-11-09
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/284-add-greeting-blake2s-library-helper/

## Overview

Follow `greeting_blake2s`. Call `greet(name)`, which validates the name, encode the completed greeting as UTF-8, and return `hashlib.shake_128(...).hexdigest(32)`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported; no new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_blake2s` and before `greeting_base32`, separated from its neighbors by two blank lines:

```python
def greeting_shake_128(name: str) -> str:
    return hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Digest length.** `hexdigest(32)` yields 32 bytes as 64 lowercase hexadecimal characters. The length is fixed; no parameter is exposed.
- **Encoding.** UTF-8 of the complete greeting, including `Hello, `; no Unicode normalization.
- **Return type.** `str`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_shake_128 as greeting_shake_128` immediately after the `greeting_sha512` import, before the `greeting_space_count` import;
- add `"greeting_shake_128"` to `__all__` immediately after `"greeting_sha512"`, before `"greeting_space_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_shake_128,` to the import list immediately after `greeting_sha512,`, before `greeting_space_count,`;
- add the example `greeting_shake_128("Ada")  # "a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774"` immediately after the `greeting_blake2s("Ada")` example;
- add this exact prose line immediately after the `greeting_blake2s` prose line:

```markdown
`greeting_shake_128` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHAKE-128 output from `hashlib.shake_128` with a fixed 32-byte length as 64 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- three independent acceptance scenarios go in `tests/features/add_greeting_shake_128_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_shake_128_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_shake_128(name: str) -> str` | Valid nonblank string name | 64-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)`; see AC1 for exact results for `"Ada"` and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Fixed 32-byte `hexdigest(32)` | Selected | Matches the 64-character width of `greeting_sha256`, `greeting_sha3_256`, and `greeting_blake2s`; deterministic single-argument API |
| Caller-selectable length parameter | Rejected | Out of scope; would change the single-argument helper shape |
| `hashlib.shake_256` | Rejected | Out of scope; a separate helper |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #296 | 2026-11-09 | Initial feature design |
