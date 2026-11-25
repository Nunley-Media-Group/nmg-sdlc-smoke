# Design: Add greeting_uppercase library helper

**Issue**: #371
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Overview

Apply `str.upper()` to the existing `greet(name)` result, export the helper from the package root, and document it in the README Library section. The change adds no import, module, or runtime dependency, and leaves the CLI unchanged.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_capitalize` and before the next function, with the same two-blank-line spacing as its neighbors:

```python
def greeting_uppercase(name: str) -> str:
    return greet(name).upper()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Case rule.** Python 3.12 `str.upper()` applies full Unicode case mapping (`ß` → `SS`); uncased characters are unchanged and no normalization is applied. This is the same transform `nmg-smoke --uppercase` applies in `src/nmg_sdlc_smoke/cli.py`, which stays unchanged.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_unique_char_count` < `greeting_uppercase` < `greeting_uppercase_count`):

- add `from .greet import greeting_uppercase as greeting_uppercase` immediately after the `greeting_unique_char_count` import;
- add `"greeting_uppercase"` to `__all__` immediately after `"greeting_unique_char_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_uppercase,` to the import list immediately after `greeting_unique_char_count,`;
- add the example `greeting_uppercase("Ada")  # "HELLO, ADA"` immediately after the `greeting_capitalize("Ada Lovelace")  # "Hello, ada lovelace"` example;
- add this exact prose line immediately after the `greeting_capitalize` prose line:

```markdown
`greeting_uppercase` returns `str.upper()` of the complete greeting (not the name alone), including the `Hello, ` prefix, using full Unicode upper-casing so a character such as `ß` expands to `SS` while uncased characters are unchanged (for example `Ada` gives `HELLO, ADA`); it matches `nmg-smoke --uppercase` output without the trailing newline, applies no Unicode normalization, and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: four independent acceptance scenarios go in `tests/features/add_greeting_uppercase_library_helper.feature`, with steps in `tests/features/steps/test_greeting_uppercase_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_uppercase(name: str) -> str` | Valid nonblank string name | `greet(name).upper()`. Invalid input raises `ValueError("name must not be blank")` | See AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greet(name).upper()` | Selected | One-line pattern identical to `greeting_swapcase`, `greeting_titlecase`, and `greeting_capitalize`; reuses validation |
| `"HELLO, " + name.upper()` after validation | Rejected | Duplicates the greeting format and validation instead of reusing `greet` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #371 | 2026-11-25 | Initial feature design |
