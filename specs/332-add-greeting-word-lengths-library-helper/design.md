# Design: Add greeting_word_lengths library helper

**Issue**: #332
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## Overview

Build the result with a list comprehension over the existing `greeting_words(name)`, using only built-ins. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_words` and before `greeting_initials`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_word_lengths(name: str) -> list[int]:
    return [len(word) for word in greeting_words(name)]
```

- **Validation.** `greeting_words` calls `greet(name)` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments, so runs of any whitespace separate words and no empty words appear. Every value is therefore at least 1.
- **Code points.** `len()` of a `str` counts code points. A decomposed `"e\u0308"` counts as two, and a non-BMP character counts as one. No normalization runs.
- **Type.** The comprehension returns a fresh built-in `list` of `int`, so `type(result) is list` holds.

In `src/nmg_sdlc_smoke/__init__.py`, keep the existing order (`greeting_word_count` < `greeting_word_lengths` < `greeting_words`):

- add `from .greet import greeting_word_lengths as greeting_word_lengths` immediately after the `greeting_word_count` import;
- add `"greeting_word_lengths"` to `__all__` immediately after `"greeting_word_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_word_lengths,` to the import list immediately after `greeting_word_count,`;
- add the example `greeting_word_lengths("Ada")  # [6, 3]` immediately after the `greeting_words("Ada")` example;
- add this exact prose line immediately after the `greeting_words` prose line:

```markdown
`greeting_word_lengths` returns a new `list[int]` with the length in Unicode code points of each whitespace-separated word of the complete greeting (not the name alone), in order, using the same `str.split()` words as `greeting_words` so runs of any whitespace separate words, no empty words appear, and punctuation stays attached (for example `Ada` gives `[6, 3]`); no Unicode normalization is applied, its length always equals `greeting_word_count`, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: six independent acceptance scenarios go in `tests/features/add_greeting_word_lengths_library_helper.feature`, with steps in `tests/features/steps/test_greeting_word_lengths_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_word_lengths(name: str) -> list[int]` | Valid nonblank string name | New `list` of positive `int` code-point word lengths. Invalid input raises `ValueError("name must not be blank")` | `str.split()` words of the complete greeting, in order, no normalization; see AC1–AC4 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Comprehension over `greeting_words(name)` | Selected | Reuses the existing split rule, so the helper agrees with `greeting_words` and `greeting_word_count` by construction |
| `list(map(len, greet(name).split()))` | Rejected | Correct, but duplicates the split rule that `greeting_words` already owns |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #332 | 2026-11-20 | Initial feature design |
