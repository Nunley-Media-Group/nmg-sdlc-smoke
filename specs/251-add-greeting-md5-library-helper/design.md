# Design: Add greeting_md5 library helper

**Issue**: #251
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/206-add-greeting-sha256-library-helper/

## Overview

Follow `greeting_sha256`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `hashlib.md5(...).hexdigest()`. Export the helper from the package root and document it in the README Library section. `hashlib` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_sha256`, separated from its neighbors by two blank lines:

```python
def greeting_md5(name: str) -> str:
    return hashlib.md5(greet(name).encode("utf-8")).hexdigest()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** `hexdigest()` returns a 32-character lowercase hexadecimal `str`.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_md5 as greeting_md5` immediately after the `greeting_lowercase_count` import;
- add `"greeting_md5"` to `__all__` immediately after `"greeting_lowercase_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_md5,` to the import list immediately after `greeting_lowercase_count,`;
- add the example `greeting_md5("Ada")  # "a4f502ca98cce831af61b0fe0a319382"` immediately after the `greeting_sha256("Ada")` example;
- add this exact prose line immediately after the `greeting_sha256` prose line:

```markdown
`greeting_md5` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its MD5 digest from `hashlib.md5` as 32 lowercase hexadecimal characters; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different digests, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_md5_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_md5_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_md5(name: str) -> str` | Valid nonblank string name | 32-character lowercase hex `str`. Invalid input raises `ValueError("name must not be blank")` | MD5 of the UTF-8 bytes of `greet(name)`: `"Ada"` → `a4f502ca98cce831af61b0fe0a319382`, `"Ada Lovelace"` → `bd0b2e5ea5baf6775e93262ce37d5a4a`, `"Zoë"` → `26ed66c6559b1e033c70ef2301fe0beb` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `hashlib.md5(greet(name).encode("utf-8")).hexdigest()` | Selected | Standard library; already imported; one-line style matches `greeting_sha256` |
| `hashlib.new("md5", ...)` | Rejected | Indirect, and inconsistent with `greeting_sha256` |
| Return raw `digest()` bytes | Rejected | The issue requires a hex `str` and puts raw bytes out of scope |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #251 | 2026-10-25 | Initial feature design |
