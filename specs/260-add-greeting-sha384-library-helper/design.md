# Design: Add greeting_sha384 library helper

**Issue**: #260
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/257-add-greeting-sha512-library-helper/

## Overview

Follow `greeting_sha512`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.sha384(...).hexdigest()`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_sha512`, separated from its neighbors by two blank lines:

```python
def greeting_sha384(name: str) -> str:
    return hashlib.sha384(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 96-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_sha384 as greeting_sha384` immediately after the `greeting_sha256` import, before the `greeting_sha512` import;
- add `"greeting_sha384"` to `__all__` immediately after `"greeting_sha256"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_sha384,` to the import list immediately after `greeting_sha256,`;
- add the example `greeting_sha384("Ada")  # "81cbed2fa5e07b7ec1d2a13da4de9584c07ddbbb2748dc5711aaafb067c07b03c120099ddcd53135b382c0e3c6198f5d"` immediately after the `greeting_sha512("Ada")` example;
- add this exact prose line immediately after the `greeting_sha512` prose line:

```markdown
`greeting_sha384` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-384 digest from `hashlib.sha384` as 96 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_sha384_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_sha384_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_sha384(name: str) -> str` | Valid nonblank string name | 96-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | SHA-384 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact digests of `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.sha384(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches `greeting_sha512` and `greeting_sha256` |
| `hashlib.new("sha384", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| Return raw `digest()` bytes | Rejected | The issue requires a hex `str` and puts raw bytes out of scope |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #260 | 2026-10-25 | Initial feature design |
