# Design: Add greeting_nfkd library helper

**Issue**: #358
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Return the NFKD normalization of `greet(name)` using the `unicodedata` module that `greet.py` already imports. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

**Placement anchor.** Each insertion below goes immediately after the `greeting_nfkc` entry when that helper exists in the file, and otherwise immediately after the `greeting_nfd` entry. This keeps alphabetical order (`greeting_nfd` < `greeting_nfkc` < `greeting_nfkd` < `greeting_punctuation_count`).

In `src/nmg_sdlc_smoke/greet.py`, add the function after the anchor function and before `greeting_reversed`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_nfkd(name: str) -> str:
    return unicodedata.normalize("NFKD", greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Compatibility then decomposition.** NFKD applies compatibility mappings (`ﬁ` → `fi`, fullwidth → ASCII, `²` → `2`) and full canonical decomposition (`é` → `e` + U+0301). Case is untouched and runs of regular spaces are not collapsed.
- **Idempotent.** Already-normalized greetings are returned equal to `greet(name)`. This includes every ASCII greeting and already-decomposed names.

In `src/nmg_sdlc_smoke/__init__.py`:

- add `from .greet import greeting_nfkd as greeting_nfkd` immediately after the anchor import;
- add `"greeting_nfkd"` to `__all__` immediately after the anchor entry;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_nfkd,` to the import list immediately after the anchor name;
- add the example `greeting_nfkd("\ufb01ona")  # "Hello, fiona"` immediately after the anchor helper's example line. The source keeps the `\ufb01` escape so the block stays ASCII-safe to execute;
- add this exact prose line immediately after the anchor helper's prose line:

```markdown
`greeting_nfkd` returns the complete greeting (not the name alone), including the `Hello, ` prefix, in Unicode Normalization Form KD using `unicodedata.normalize("NFKD", ...)`, so compatibility characters are replaced by their compatibility equivalents (for example `ﬁona` gives `Hello, fiona`, full-width `Ａda` gives `Hello, Ada`, and `Ada²` gives `Hello, Ada2`) and precomposed characters are decomposed into a base character followed by combining marks (for example `Chloé` gives `Hello, Chloe` plus U+0301, 13 code points); already-normalized text is unchanged, no case change, whitespace collapsing, or accent stripping is made, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: six independent acceptance scenarios go in `tests/features/add_greeting_nfkd_library_helper.feature`, with steps in `tests/features/steps/test_greeting_nfkd_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_nfkd(name: str) -> str` | Valid nonblank string name | NFKD-normalized greeting. Invalid input raises `ValueError("name must not be blank")` | Equals `unicodedata.normalize("NFKD", greet(name))`; see AC1–AC4 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `unicodedata.normalize("NFKD", greet(name))` | Selected | Standard library, exactly the AC4 oracle, reuses the existing import |
| `"Hello, " + unicodedata.normalize("NFKD", name)` | Rejected | Duplicates `greet` formatting and skips its validation |
| Reuse `greeting_slug` internals | Rejected | The slug strips combining marks and lowercases, which violates AC2 and AC3 |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #358 | 2026-11-23 | Initial feature design |
