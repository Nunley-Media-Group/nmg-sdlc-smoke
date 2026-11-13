# Design: Add greeting_shake_256 library helper

**Issue**: #299
**Date**: 2026-11-13
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/296-add-greeting-shake-128-library-helper/

## Overview

Follow `greeting_shake_128`. Call `greet(name)`, which validates the name, encode the completed greeting as UTF-8, and return `hashlib.shake_256(...).hexdigest(64)`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported; no new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_shake_128` and before `greeting_base32`, separated from its neighbors by two blank lines:

```python
def greeting_shake_256(name: str) -> str:
    return hashlib.shake_256(greet(name).encode("utf-8")).hexdigest(64)
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Digest length.** `hexdigest(64)` yields 64 bytes as 128 lowercase hexadecimal characters. The length is fixed; no parameter is exposed.
- **Encoding.** UTF-8 of the complete greeting, including `Hello, `; no Unicode normalization.
- **Return type.** `str`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_shake_256 as greeting_shake_256` immediately after the `greeting_shake_128` import, before the `greeting_space_count` import;
- add `"greeting_shake_256"` to `__all__` immediately after `"greeting_shake_128"`, before `"greeting_space_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_shake_256,` to the import list immediately after `greeting_shake_128,`;
- add the example `greeting_shake_256("Ada")  # "51412b094871bbe3e276da7fa1fad8bd4bfae7cfbeb88db9e732d1f32461e67c41e270771c528e629790ba47af4772e92632de0b5b8f63cf801ef7eb8d6a29a7"` immediately after the `greeting_shake_128("Ada")` example;
- add this exact prose line immediately after the `greeting_shake_128` prose line:

```markdown
`greeting_shake_256` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHAKE-256 output from `hashlib.shake_256` with a fixed 64-byte length as 128 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- three independent acceptance scenarios go in `tests/features/add_greeting_shake_256_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_shake_256_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_shake_256(name: str) -> str` | Valid nonblank string name | 128-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | `hashlib.shake_256(greet(name).encode("utf-8")).hexdigest(64)`; see AC1 for exact results for `"Ada"` and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Fixed 64-byte `hexdigest(64)` | Selected | Matches SHAKE-256's 256-bit security level and the 128-character width of `greeting_sha512`, `greeting_sha3_512`, and `greeting_blake2b`; deterministic single-argument API |
| Fixed 32-byte `hexdigest(32)` | Rejected | Issue #299 fixes the output at 64 bytes |
| Caller-selectable length parameter | Rejected | Out of scope; would change the single-argument helper shape |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #299 | 2026-11-13 | Initial feature design |
