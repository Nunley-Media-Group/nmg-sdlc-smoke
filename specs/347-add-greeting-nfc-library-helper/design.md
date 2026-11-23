# Design: Add greeting_nfc library helper

**Issue**: #347
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## Overview

Return the NFC normalization of `greet(name)` using the `unicodedata` module that `greet.py` already imports. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_swapcase` and before `greeting_reversed`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_nfc(name: str) -> str:
    return unicodedata.normalize("NFC", greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Canonical only.** NFC composes canonical equivalents and never applies compatibility mappings, so `ﬁ` (U+FB01) stays and whitespace and case are untouched.
- **Idempotent.** Already-NFC greetings (including every ASCII greeting) are returned equal to `greet(name)`.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_md5` < `greeting_nfc` < `greeting_punctuation_count`):

- add `from .greet import greeting_nfc as greeting_nfc` immediately after the `greeting_md5` import;
- add `"greeting_nfc"` to `__all__` immediately after `"greeting_md5"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_nfc,` to the import list immediately after `greeting_md5,`;
- add the example `greeting_nfc("Chloe\u0301")  # "Hello, Chloé"` immediately after the `greeting_swapcase("Ada")  # "hELLO, aDA"` example (the source keeps the `\u0301` escape so the block stays ASCII-safe to execute);
- add this exact prose line immediately after the `greeting_swapcase` prose line:

```markdown
`greeting_nfc` returns the complete greeting (not the name alone), including the `Hello, ` prefix, in Unicode Normalization Form C using `unicodedata.normalize("NFC", ...)`, so a base character followed by combining marks is composed into its precomposed form where one exists (for example `Chloe` plus U+0301 gives `Hello, Chloé`) and already-composed text is unchanged; only canonical composition is applied, so compatibility characters such as `ﬁ` are kept and no case, whitespace, or accent stripping change is made, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: six independent acceptance scenarios go in `tests/features/add_greeting_nfc_library_helper.feature`, with steps in `tests/features/steps/test_greeting_nfc_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_nfc(name: str) -> str` | Valid nonblank string name | NFC-normalized greeting. Invalid input raises `ValueError("name must not be blank")` | Equals `unicodedata.normalize("NFC", greet(name))`; see AC1–AC4 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `unicodedata.normalize("NFC", greet(name))` | Selected | Standard library, exactly the AC4 oracle, reuses the existing import |
| `"Hello, " + unicodedata.normalize("NFC", name)` | Rejected | Duplicates `greet` formatting and skips its validation |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #347 | 2026-11-22 | Initial feature design |
