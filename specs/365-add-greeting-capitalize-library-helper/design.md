# Design: Add greeting_capitalize library helper

**Issue**: #365
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Apply `str.capitalize()` to the existing `greet(name)` result, export the helper from the package root, and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_titlecase` and before `greeting_nfc`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_capitalize(name: str) -> str:
    return greet(name).capitalize()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Case rule.** Python 3.12 `str.capitalize()` titlecases the first character (always `H`) and lowercases the rest with `str.lower()` rules; uncased characters are unchanged. No normalization is applied.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_bytes` < `greeting_capitalize` < `greeting_casefold`):

- add `from .greet import greeting_capitalize as greeting_capitalize` immediately after the `greeting_bytes` import;
- add `"greeting_capitalize"` to `__all__` immediately after `"greeting_bytes"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_capitalize,` to the import list immediately after `greeting_bytes,`;
- add the example `greeting_capitalize("Ada Lovelace")  # "Hello, ada lovelace"` immediately after the `greeting_titlecase("ada lovelace")  # "Hello, Ada Lovelace"` example;
- add this exact prose line immediately after the `greeting_titlecase` prose line:

```markdown
`greeting_capitalize` returns `str.capitalize()` of the complete greeting (not the name alone), including the `Hello, ` prefix, so the first character stays uppercase and every other cased character becomes lowercase while uncased characters are unchanged (for example `Ada Lovelace` gives `Hello, ada lovelace`); no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: four independent acceptance scenarios go in `tests/features/add_greeting_capitalize_library_helper.feature`, with steps in `tests/features/steps/test_greeting_capitalize_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_capitalize(name: str) -> str` | Valid nonblank string name | `greet(name).capitalize()`. Invalid input raises `ValueError("name must not be blank")` | See AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greet(name).capitalize()` | Selected | One-line pattern identical to `greeting_swapcase` and `greeting_titlecase`; reuses validation |
| `"Hello, " + name.lower()` after validation | Rejected | Duplicates the greeting format and validation instead of reusing `greet` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #365 | 2026-11-23 | Initial feature design |
