# Design: Add greeting_word_frequency library helper

**Issue**: #362
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Count the elements of the existing `greeting_words(name)` list into a new plain `dict`, in first-seen order. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_last_word` and before `greeting_initials`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_word_frequency(name: str) -> dict[str, int]:
    frequency: dict[str, int] = {}
    for word in greeting_words(name):
        frequency[word] = frequency.get(word, 0) + 1
    return frequency
```

- **Validation.** `greeting_words` calls `greet(name)` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments, so whitespace handling is identical to `greeting_words` and `greeting_word_count`.
- **Exact keys and order.** Words are used unchanged as keys: no case folding, no normalization, punctuation kept. Python `dict` insertion order gives first-seen ordering.
- **Fresh result.** A new `dict` is built on every call, and it is a plain `dict` (not `collections.Counter`), matching `greeting_char_frequency`.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_word_count` < `greeting_word_frequency` < `greeting_word_lengths`):

- add `from .greet import greeting_word_frequency as greeting_word_frequency` immediately after the `greeting_word_count` import;
- add `"greeting_word_frequency"` to `__all__` immediately after `"greeting_word_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_word_frequency,` to the import list immediately after `greeting_word_count,`;
- add the example `greeting_word_frequency("Bo Bo")  # {"Hello,": 1, "Bo": 2}` immediately after the `greeting_last_word("Ada Lovelace")  # 'Lovelace'` example;
- add this exact prose line immediately after the `greeting_last_word` prose line:

```markdown
`greeting_word_frequency` returns a new plain `dict[str, int]` mapping each whitespace-separated word of the complete greeting (not the name alone) to the number of times it occurs, using the same `str.split()` words as `greeting_words`; keys are the words unchanged and case-sensitive, with punctuation attached and no Unicode normalization, and appear in the order each word first occurs (for example `Bo Bo` gives `{"Hello,": 1, "Bo": 2}`), so the values always sum to `greeting_word_count(name)`, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: seven independent acceptance scenarios go in `tests/features/add_greeting_word_frequency_library_helper.feature`, with steps in `tests/features/steps/test_greeting_word_frequency_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_word_frequency(name: str) -> dict[str, int]` | Valid nonblank string name | New plain dict of word → count in first-seen order. Invalid input raises `ValueError("name must not be blank")` | Counts `greeting_words(name)`; see AC1–AC5 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Loop over `greeting_words(name)` into a plain dict | Selected | Reuses the split rule and validation, returns `type(result) is dict`, and mirrors `greeting_char_frequency` |
| `collections.Counter(greeting_words(name))` | Rejected | Returns a `Counter` subclass, which breaks `type(result) is dict` |
| `dict(Counter(...))` | Rejected | Adds an import for no behavioral gain over the loop |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #362 | 2026-11-23 | Initial feature design |
