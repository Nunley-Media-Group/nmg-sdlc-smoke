# Design: Add greeting_sha224 library helper

**Issue**: #266
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/260-add-greeting-sha384-library-helper/

## Overview

Follow `greeting_sha384`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.sha224(...).hexdigest()`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_sha384`, separated from its neighbors by two blank lines:

```python
def greeting_sha224(name: str) -> str:
    return hashlib.sha224(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 56-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_sha224 as greeting_sha224` immediately after the `greeting_sha1` import, before the `greeting_sha256` import;
- add `"greeting_sha224"` to `__all__` immediately after `"greeting_sha1"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_sha224,` to the import list immediately after `greeting_sha1,`;
- add the example `greeting_sha224("Ada")  # "316233754fcc3ee5160b0102d33639e694a894f689633ca5d2d679ad"` immediately after the `greeting_sha384("Ada")` example;
- add this exact prose line immediately after the `greeting_sha384` prose line:

```markdown
`greeting_sha224` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-224 digest from `hashlib.sha224` as 56 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_sha224_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_sha224_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_sha224(name: str) -> str` | Valid nonblank string name | 56-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | SHA-224 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact digests of `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.sha224(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches `greeting_sha384` and `greeting_sha256` |
| `hashlib.new("sha224", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| Truncate `greeting_sha256` output | Rejected | SHA-224 uses different initial values, so a truncated SHA-256 is not a SHA-224 digest |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #266 | 2026-10-25 | Initial feature design |
