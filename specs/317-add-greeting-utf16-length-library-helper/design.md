# Design: Add greeting_utf16_length library helper

**Issue**: #317
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/314-add-greeting-codepoints-library-helper/

## Overview

Follow `greeting_bytes`. Call `greet(name)`, which validates the name. Encode the completed greeting as BOM-less `utf-16-le` and return the byte length divided by two. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_codepoints` and before `greeting_is_ascii`, using the same blank-line spacing as its neighbors:

```python
def greeting_utf16_length(name: str) -> int:
    return len(greet(name).encode("utf-16-le")) // 2
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Transform.** Encoding with `utf-16-le` writes no byte-order mark. Every code unit is exactly two bytes, so the byte length divided by two is the code-unit count. A BMP character contributes one unit. A non-BMP character contributes two units (a surrogate pair). No Unicode normalization is applied.
- **Return type.** A plain `int`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_utf16_length as greeting_utf16_length` immediately after the `greeting_url_encoded` import and before the `greeting_vowel_count` import;
- add `"greeting_utf16_length"` to `__all__` immediately after `"greeting_url_encoded"` and before `"greeting_vowel_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_utf16_length,` to the import list immediately after `greeting_uppercase_count,` and before `greeting_vowel_count,`;
- add the example `greeting_utf16_length("Ada")  # 10` immediately after the `greeting_codepoints("Ada")` example;
- add this exact prose line immediately after the `greeting_codepoints` prose line:

```markdown
`greeting_utf16_length` returns the number of UTF-16 code units in the complete greeting (not the name alone), including the `Hello, ` prefix and excluding any byte-order mark, so a character outside the Basic Multilingual Plane counts as two units (for example `Ada` gives `10` and `😀` gives `9`); no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_utf16_length_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_utf16_length_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_utf16_length(name: str) -> int` | Valid nonblank string name | `int`. Invalid input raises `ValueError("name must not be blank")` | `len(greet(name).encode("utf-16-le")) // 2`; see AC1 and AC2 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `len(encode("utf-16-le")) // 2` | Selected | Standard library, writes no BOM, and is deterministic on every platform |
| `encode("utf-16")` | Rejected | Adds a two-byte BOM that would inflate the count |
| `sum(2 if ord(ch) > 0xFFFF else 1 ...)` | Rejected | Duplicates codec logic that the encoder already applies |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #317 | 2026-11-15 | Initial feature design |
