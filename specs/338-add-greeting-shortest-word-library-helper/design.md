# Design: Add greeting_shortest_word library helper

**Issue**: #338
**Date**: 2026-11-20
**Status**: Approved
**Author**: NMG

## Overview

Select the result with the built-in `min(..., key=len)` over the existing `greeting_words(name)`. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_longest_word` and before `greeting_initials`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_shortest_word(name: str) -> str:
    return min(greeting_words(name), key=len)
```

- **Validation.** `greeting_words` calls `greet(name)` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments. The list always contains `Hello,`, so it is never empty and `min` never raises on an empty sequence.
- **Tie rule.** `min` returns the first minimal element in iteration order, so the earliest word wins a length tie.
- **Code points.** `len()` of a `str` counts code points. A decomposed `"e\N{COMBINING ACUTE ACCENT}"` counts as two, and no normalization runs. The returned word is the original `str` object from the split, so it is returned unchanged.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_shake_256` < `greeting_shortest_word` < `greeting_slug`):

- add `from .greet import greeting_shortest_word as greeting_shortest_word` immediately after the `greeting_shake_256` import;
- add `"greeting_shortest_word"` to `__all__` immediately after `"greeting_shake_256"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_shortest_word,` to the import list immediately after `greeting_shake_256,`;
- add the example `greeting_shortest_word("Ada")  # 'Ada'` immediately after the `greeting_longest_word("Ada")  # 'Hello,'` example;
- add this exact prose line immediately after the `greeting_longest_word` prose line:

```markdown
`greeting_shortest_word` returns the shortest whitespace-separated word of the complete greeting (not the name alone) as a `str`, using the same `str.split()` words as `greeting_words` with punctuation attached and length measured in Unicode code points with no normalization; when several words share the smallest length the first one wins (for example `Ada` gives `Ada` and `Bertha` gives `Hello,`), and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: eight independent acceptance scenarios go in `tests/features/add_greeting_shortest_word_library_helper.feature`, with steps in `tests/features/steps/test_greeting_shortest_word_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_shortest_word(name: str) -> str` | Valid nonblank string name | The shortest `str` word of the greeting. Invalid input raises `ValueError("name must not be blank")` | `str.split()` words of the complete greeting, code-point length, first wins on a tie; see AC1–AC6 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `min(greeting_words(name), key=len)` | Selected | Reuses the existing split rule, and `min` already returns the first of several tied words |
| `sorted(words, key=len)[0]` | Rejected | Gives the same result but sorts the whole list for no benefit |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #338 | 2026-11-20 | Initial feature design |
