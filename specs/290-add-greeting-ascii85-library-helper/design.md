# Design: Add greeting_ascii85 library helper

**Issue**: #290
**Date**: 2026-11-07
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/287-add-greeting-base85-library-helper/

## Overview

Follow `greeting_base85`. Call `greet(name)`, which validates the name, then encode the completed greeting as UTF-8 and return `base64.a85encode(...).decode("ascii")` with default arguments. Export the helper from the package root and document it in the README Library section. `base64` is already imported in `greet.py`, so this adds no new import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_base85` and before `greeting_rot13`, separated from its neighbors by two blank lines:

```python
def greeting_ascii85(name: str) -> str:
    return base64.a85encode(greet(name).encode("utf-8")).decode("ascii")
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 with no Unicode normalization, so `ë` contributes the bytes `C3 AB`.
- **Return type.** With its defaults (`foldspaces=False`, `wrapcol=0`, `pad=False`, `adobe=False`), `a85encode` returns ASCII `bytes` with no `<~ ~>` delimiters, no `y` folding, and no line wrapping. `.decode("ascii")` turns that into a `str`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add the self-aliased import `from .greet import greeting_ascii85 as greeting_ascii85` immediately after the `greeting_adler32` import, before the `greeting_base32` import;
- add `"greeting_ascii85"` to `__all__` immediately after `"greeting_adler32"`, before `"greeting_base32"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_ascii85,` to the import list immediately after `greeting_adler32,`, before `greeting_base32,`;
- add the example `greeting_ascii85("Ada")  # "87cURD_*\"sA75"` immediately after the `greeting_base85("Ada")` example;
- add this exact prose line immediately after the `greeting_base85` prose line:

```markdown
`greeting_ascii85` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its Ascii85 encoding from `base64.a85encode` with default arguments as a `str`, with no `<~ ~>` delimiters, no `y` folding of spaces, and no line wrapping; no Unicode normalization is applied, so precomposed and decomposed spellings of a name produce different results, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_ascii85_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_ascii85_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_ascii85(name: str) -> str` | Valid nonblank string name | Ascii85 `str` without delimiters, folding, or wrapping. Invalid input raises `ValueError("name must not be blank")` | Ascii85 of the UTF-8 bytes of `greet(name)`; see AC1 and AC2 for exact results for `"Ada"`, `"Ada Lovelace"`, and `"Zoë"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `base64.a85encode(greet(name).encode("utf-8")).decode("ascii")` | Selected | Standard library; already imported; one-line style matches `greeting_base85` |
| `a85encode(..., adobe=True)` | Rejected | Issue requires no `<~ ~>` delimiters |
| `a85encode(..., foldspaces=True)` or `wrapcol>0` | Rejected | Issue requires no `y` folding and no wrapping |
| `base64.z85encode(...)` | Rejected | Out of scope; added only in Python 3.13, not available on 3.12 |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #290 | 2026-11-07 | Initial feature design |
