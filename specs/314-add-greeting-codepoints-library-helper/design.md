# Design: Add greeting_codepoints library helper

**Issue**: #314
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/311-add-greeting-swapcase-library-helper/

## Overview

Follow `greeting_bytes`. Call `greet(name)`, which validates the name, and return a list of `ord()` values for each character of the completed greeting. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_bytes` and before `greeting_is_ascii`, using the same blank-line spacing as its neighbors:

```python
def greeting_codepoints(name: str) -> list[int]:
    return [ord(ch) for ch in greet(name)]
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Transform.** `ord()` of each character of the complete greeting, including `Hello, `. Python `str` iteration yields code points, so a non-BMP character yields exactly one value. No Unicode normalization is applied.
- **Return type.** A newly built `list[int]` on every call.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_codepoints as greeting_codepoints` immediately after the `greeting_casefold` import and before the `greeting_crc32` import;
- add `"greeting_codepoints"` to `__all__` immediately after `"greeting_casefold"` and before `"greeting_crc32"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_codepoints,` to the import list immediately after `greeting_casefold,`;
- add the example `greeting_codepoints("Ada")  # [72, 101, 108, 108, 111, 44, 32, 65, 100, 97]` immediately after the `greeting_bytes("Ada")  # 10` example;
- add this exact prose line immediately after the `greeting_casefold` prose line:

```markdown
`greeting_codepoints` returns a new `list[int]` of `ord()` values for each character of the complete greeting (not the name alone), including the `Hello, ` prefix, so a character outside the Basic Multilingual Plane contributes exactly one code point (for example `Ada` gives `[72, 101, 108, 108, 111, 44, 32, 65, 100, 97]`); no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_codepoints_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_codepoints_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_codepoints(name: str) -> list[int]` | Valid nonblank string name | `list[int]`. Invalid input raises `ValueError("name must not be blank")` | `[ord(ch) for ch in greet(name)]`; see AC1 and AC2 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `list[int]` of `ord()` values | Selected | Fixed by issue #314; standard library and deterministic |
| `U+XXXX` formatted string | Rejected | Out of scope per issue #314 |
| `tuple[int, ...]` | Rejected | Issue #314 fixes the return type as `list[int]` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #314 | 2026-11-15 | Initial feature design |
