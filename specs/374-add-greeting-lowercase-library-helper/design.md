# Design: Add greeting_lowercase library helper

**Issue**: #374
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Overview

Apply `str.lower()` to the existing `greet(name)` result, export the helper from the package root, and document it in the README Library section. The change adds no import, module, or runtime dependency, and the CLI stays unchanged.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_uppercase` and before `greeting_nfc`, with the same two-blank-line spacing as the functions around it:

```python
def greeting_lowercase(name: str) -> str:
    return greet(name).lower()
```

- **Validation.** `greet(name)` runs first, so invalid names raise its `ValueError("name must not be blank")` unchanged.
- **Case rule.** Python 3.12 `str.lower()` lowers cased characters without case folding (`ß` stays `ß`, unlike `greeting_casefold`). Uncased characters are unchanged, and no normalization is applied. `nmg-smoke --lowercase` applies the same transform in `src/nmg_sdlc_smoke/cli.py`, and that file stays unchanged.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_longest_word` < `greeting_lowercase` < `greeting_lowercase_count`):

- add `from .greet import greeting_lowercase as greeting_lowercase` immediately after the `greeting_longest_word` import;
- add `"greeting_lowercase"` to `__all__` immediately after `"greeting_longest_word"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_lowercase,` to the import list immediately after `greeting_longest_word,`;
- add the example `greeting_lowercase("Ada")  # "hello, ada"` immediately after the `greeting_uppercase("Ada")  # "HELLO, ADA"` example;
- add this exact prose line immediately after the `greeting_uppercase` prose line:

```markdown
`greeting_lowercase` returns `str.lower()` of the complete greeting (not the name alone), including the `Hello, ` prefix, so cased characters become lowercase without case folding (for example `Ada` gives `hello, ada` and `Straße` keeps its `ß` as `hello, straße`) while uncased characters are unchanged; it matches `nmg-smoke --lowercase` output without the trailing newline, applies no Unicode normalization, and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: four independent acceptance scenarios go in `tests/features/add_greeting_lowercase_library_helper.feature`, with steps in `tests/features/steps/test_greeting_lowercase_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_lowercase(name: str) -> str` | Valid nonblank string name | `greet(name).lower()`. Invalid input raises `ValueError("name must not be blank")` | See AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greet(name).lower()` | Selected | Same one-line pattern as `greeting_uppercase`, `greeting_swapcase`, and `greeting_capitalize`; reuses validation |
| `greet(name).casefold()` | Rejected | Already provided by `greeting_casefold`, and differs from `nmg-smoke --lowercase` (`ß` → `ss`) |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #374 | 2026-11-25 | Initial feature design |
