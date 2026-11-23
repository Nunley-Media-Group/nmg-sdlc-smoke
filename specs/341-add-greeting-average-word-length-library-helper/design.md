# Design: Add greeting_average_word_length library helper

**Issue**: #341
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## Overview

Compute the mean from the existing `greeting_word_lengths(name)` and `greeting_words(name)` helpers with true division. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_shortest_word` and before `greeting_initials`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_average_word_length(name: str) -> float:
    return sum(greeting_word_lengths(name)) / len(greeting_words(name))
```

- **Validation.** `greeting_word_lengths` calls `greet(name)` through `greeting_words` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged before any division runs.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments. The list always contains `Hello,` and at least one name word, so the divisor is never zero.
- **Float result.** `/` is true division, so the result is a `float` even when the mean is whole (`12 / 2 == 6.0`). No rounding is applied.
- **Code points.** `len()` of a `str` counts code points. A decomposed `"e\N{COMBINING ACUTE ACCENT}"` counts as two, and no normalization runs.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_ascii85` < `greeting_average_word_length` < `greeting_base32`):

- add `from .greet import greeting_average_word_length as greeting_average_word_length` immediately after the `greeting_ascii85` import;
- add `"greeting_average_word_length"` to `__all__` immediately after `"greeting_ascii85"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_average_word_length,` to the import list immediately after `greeting_ascii85,`;
- add the example `greeting_average_word_length("Ada")  # 4.5` immediately after the `greeting_shortest_word("Ada")  # 'Ada'` example;
- add this exact prose line immediately after the `greeting_shortest_word` prose line:

```markdown
`greeting_average_word_length` returns the mean length of the whitespace-separated words of the complete greeting (not the name alone) as an unrounded `float`, using the same `str.split()` words as `greeting_words` with punctuation attached and length measured in Unicode code points with no normalization (for example `Ada` gives `4.5` and `Bertha` gives `6.0`), and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: seven independent acceptance scenarios go in `tests/features/add_greeting_average_word_length_library_helper.feature`, with steps in `tests/features/steps/test_greeting_average_word_length_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_average_word_length(name: str) -> float` | Valid nonblank string name | Unrounded `float` mean word length of the greeting. Invalid input raises `ValueError("name must not be blank")` | `str.split()` words of the complete greeting, code-point length, true division; see AC1–AC5 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `sum(greeting_word_lengths(name)) / len(greeting_words(name))` | Selected | Reuses the existing split and length rules, and is exactly the AC5 oracle |
| `statistics.fmean(greeting_word_lengths(name))` | Rejected | Adds an import and may differ from the AC5 expression in the last floating-point bit |
| `round(mean, 2)` | Rejected | The issue requires an unrounded result |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #341 | 2026-11-22 | Initial feature design |
