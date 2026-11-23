# Design: Add greeting_nfd library helper

**Issue**: #350
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Return the NFD normalization of `greet(name)` using the `unicodedata` module that `greet.py` already imports. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_nfc` and before `greeting_reversed`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_nfd(name: str) -> str:
    return unicodedata.normalize("NFD", greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Canonical only.** NFD decomposes canonical equivalents and never applies compatibility mappings, so `ﬁ` (U+FB01) stays and whitespace and case are untouched.
- **Idempotent.** Greetings with no decomposable characters (including every ASCII greeting and already-decomposed names) are returned equal to `greet(name)`.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_nfc` < `greeting_nfd` < `greeting_punctuation_count`):

- add `from .greet import greeting_nfd as greeting_nfd` immediately after the `greeting_nfc` import;
- add `"greeting_nfd"` to `__all__` immediately after `"greeting_nfc"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_nfd,` to the import list immediately after `greeting_nfc,`;
- add the example `len(greeting_nfd("Chlo\u00e9"))  # 13` immediately after the `greeting_nfc("Chloe\u0301")  # "Hello, Chloé"` example (the source keeps the `\u00e9` escape so the block stays ASCII-safe to execute);
- add this exact prose line immediately after the `greeting_nfc` prose line:

```markdown
`greeting_nfd` returns the complete greeting (not the name alone), including the `Hello, ` prefix, in Unicode Normalization Form D using `unicodedata.normalize("NFD", ...)`, so a precomposed character is decomposed into its base character followed by combining marks (for example `Chloé` gives `Hello, Chloe` plus U+0301, 13 code points) and text with no decomposable characters is unchanged; only canonical decomposition is applied, so compatibility characters such as `ﬁ` are kept and no case, whitespace, or accent stripping change is made, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: six independent acceptance scenarios go in `tests/features/add_greeting_nfd_library_helper.feature`, with steps in `tests/features/steps/test_greeting_nfd_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_nfd(name: str) -> str` | Valid nonblank string name | NFD-normalized greeting. Invalid input raises `ValueError("name must not be blank")` | Equals `unicodedata.normalize("NFD", greet(name))`; see AC1–AC4 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `unicodedata.normalize("NFD", greet(name))` | Selected | Standard library, exactly the AC4 oracle, reuses the existing import |
| `"Hello, " + unicodedata.normalize("NFD", name)` | Rejected | Duplicates `greet` formatting and skips its validation |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #350 | 2026-11-23 | Initial feature design |
