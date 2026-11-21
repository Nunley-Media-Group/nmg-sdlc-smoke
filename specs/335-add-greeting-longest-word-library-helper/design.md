# Design: Add greeting_longest_word library helper

**Issue**: #335
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## Overview

Select the result with the built-in `max(..., key=len)` over the existing `greeting_words(name)`. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_word_lengths` and before `greeting_initials`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_longest_word(name: str) -> str:
    return max(greeting_words(name), key=len)
```

- **Validation.** `greeting_words` calls `greet(name)` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments. The list always contains `Hello,`, so it is never empty and `max` never raises on an empty sequence.
- **Tie rule.** `max` returns the first maximal element in iteration order, so the earliest word wins a length tie.
- **Code points.** `len()` of a `str` counts code points. A decomposed `"e\u0301"` counts as two, and no normalization runs. The returned word is the original `str` object from the split, so it is returned unchanged.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_letter_count` < `greeting_longest_word` < `greeting_lowercase_count`):

- add `from .greet import greeting_longest_word as greeting_longest_word` immediately after the `greeting_letter_count` import;
- add `"greeting_longest_word"` to `__all__` immediately after `"greeting_letter_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_longest_word,` to the import list immediately after `greeting_letter_count,`;
- add the example `greeting_longest_word("Ada")  # 'Hello,'` immediately after the `greeting_word_lengths("Ada")  # [6, 3]` example;
- add this exact prose line immediately after the `greeting_word_lengths` prose line:

```markdown
`greeting_longest_word` returns the longest whitespace-separated word of the complete greeting (not the name alone) as a `str`, using the same `str.split()` words as `greeting_words` with punctuation attached and length measured in Unicode code points with no normalization; when several words share the greatest length the first one wins (for example `Ada` gives `Hello,` and `Ada Lovelace` gives `Lovelace`), and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: seven independent acceptance scenarios go in `tests/features/add_greeting_longest_word_library_helper.feature`, with steps in `tests/features/steps/test_greeting_longest_word_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_longest_word(name: str) -> str` | Valid nonblank string name | The longest `str` word of the greeting. Invalid input raises `ValueError("name must not be blank")` | `str.split()` words of the complete greeting, code-point length, first wins on a tie; see AC1–AC5 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `max(greeting_words(name), key=len)` | Selected | Reuses the existing split rule, and `max` already returns the first of several tied words |
| `sorted(words, key=len)[-1]` | Rejected | Sorting is stable, so it returns the last tied word, which breaks AC2 |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #335 | 2026-11-20 | Initial feature design |
