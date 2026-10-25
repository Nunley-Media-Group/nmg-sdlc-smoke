# Design: Add greeting_sha1 library helper

**Issue**: #254
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/251-add-greeting-md5-library-helper/

## Overview

Follow `greeting_md5`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.sha1(...).hexdigest()`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_md5`, separated from its neighbors by two blank lines:

```python
def greeting_sha1(name: str) -> str:
    return hashlib.sha1(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 40-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_sha1 as greeting_sha1` immediately after the `greeting_rot13` import, before the `greeting_sha256` import;
- add `"greeting_sha1"` to `__all__` immediately after `"greeting_rot13"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_sha1,` to the import list immediately after `greeting_rot13,`;
- add the example `greeting_sha1("Ada")  # "991f190147e71279d8656214e556b36a22bf73e4"` immediately after the `greeting_md5("Ada")` example;
- add this exact prose line immediately after the `greeting_md5` prose line:

```markdown
`greeting_sha1` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its SHA-1 digest from `hashlib.sha1` as 40 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_sha1_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_sha1_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_sha1(name: str) -> str` | Valid nonblank string name | 40-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | SHA-1 of the UTF-8 bytes of `greet(name)`: `"Ada"` → `991f190147e71279d8656214e556b36a22bf73e4`, `"Ada Lovelace"` → `8dde18c21e3195df968018b6213efc61d033ec4f`, `"Zoë"` → `5e2bef193596dd46528fb36c4ef8625f71c84577` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.sha1(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches `greeting_md5` and `greeting_sha256` |
| `hashlib.new("sha1", ...)` | Rejected | Indirect, and inconsistent with the sibling helpers |
| Return raw `digest()` bytes | Rejected | The issue requires a hex `str` and puts raw bytes out of scope |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #254 | 2026-10-25 | Initial feature design |
