# Design: Add greeting_nfkc library helper

**Issue**: #356
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Return the NFKC normalization of `greet(name)` using the `unicodedata` module that `greet.py` already imports. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_nfd` and before `greeting_reversed`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_nfkc(name: str) -> str:
    return unicodedata.normalize("NFKC", greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Compatibility then composition.** NFKC applies compatibility decomposition (`ﬁ` → `fi`, full-width → ASCII, U+00A0 → U+0020) followed by canonical composition (`e` + U+0301 → `é`). Case is untouched and runs of regular spaces are not collapsed.
- **Idempotent.** Already-normalized greetings, including every ASCII greeting, are returned equal to `greet(name)`.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_nfd` < `greeting_nfkc` < `greeting_punctuation_count`):

- add `from .greet import greeting_nfkc as greeting_nfkc` immediately after the `greeting_nfd` import;
- add `"greeting_nfkc"` to `__all__` immediately after `"greeting_nfd"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_nfkc,` to the import list immediately after `greeting_nfd,`;
- add the example `greeting_nfkc("ﬁona")  # "Hello, fiona"` immediately after the `len(greeting_nfd("Chloé"))  # 13` example (the source keeps the `ﬁ` escape so the block stays ASCII-safe to execute);
- add this exact prose line immediately after the `greeting_nfd` prose line:

```markdown
`greeting_nfkc` returns the complete greeting (not the name alone), including the `Hello, ` prefix, in Unicode Normalization Form KC using `unicodedata.normalize("NFKC", ...)`, so compatibility characters are replaced by their standard equivalents (for example `ﬁona` gives `Hello, fiona`, full-width `Ａｄａ` gives `Hello, Ada`, and a no-break space becomes a regular space) and the result is canonically composed (for example `Chloe` plus U+0301 gives `Hello, Chloé`); already-normalized text is unchanged, no case change, whitespace collapsing, or accent stripping is made, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: six independent acceptance scenarios go in `tests/features/add_greeting_nfkc_library_helper.feature`, with steps in `tests/features/steps/test_greeting_nfkc_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_nfkc(name: str) -> str` | Valid nonblank string name | NFKC-normalized greeting. Invalid input raises `ValueError("name must not be blank")` | Equals `unicodedata.normalize("NFKC", greet(name))`; see AC1–AC4 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `unicodedata.normalize("NFKC", greet(name))` | Selected | Standard library, exactly the AC4 oracle, reuses the existing import |
| `"Hello, " + unicodedata.normalize("NFKC", name)` | Rejected | Duplicates `greet` formatting and skips its validation |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #356 | 2026-11-23 | Initial feature design |
