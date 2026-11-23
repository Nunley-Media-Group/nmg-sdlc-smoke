# Design: Add greeting_last_word library helper

**Issue**: #344
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## Overview

Return the last element of the existing `greeting_words(name)` list. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_average_word_length` and before `greeting_initials`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_last_word(name: str) -> str:
    return greeting_words(name)[-1]
```

- **Validation.** `greeting_words` calls `greet(name)` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments. The list always contains `Hello,` and at least one name word, so `[-1]` never raises `IndexError` and is always a name word.
- **Unchanged word.** The word is returned exactly as split: attached punctuation is kept, and no case change or normalization is applied.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_is_title` < `greeting_last_word` < `greeting_length`):

- add `from .greet import greeting_last_word as greeting_last_word` immediately after the `greeting_is_title` import;
- add `"greeting_last_word"` to `__all__` immediately after `"greeting_is_title"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_last_word,` to the import list immediately after `greeting_is_title,`;
- add the example `greeting_last_word("Ada Lovelace")  # 'Lovelace'` immediately after the `greeting_average_word_length("Ada")  # 4.5` example;
- add this exact prose line immediately after the `greeting_average_word_length` prose line:

```markdown
`greeting_last_word` returns the last whitespace-separated word of the complete greeting (not the name alone) as a `str`, using the same `str.split()` words as `greeting_words` and returning that word unchanged with punctuation attached and no case change or Unicode normalization (for example `Ada` gives `Ada` and `Ada Lovelace` gives `Lovelace`), and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: six independent acceptance scenarios go in `tests/features/add_greeting_last_word_library_helper.feature`, with steps in `tests/features/steps/test_greeting_last_word_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_last_word(name: str) -> str` | Valid nonblank string name | Last `str.split()` word of the greeting, unchanged. Invalid input raises `ValueError("name must not be blank")` | Equals `greeting_words(name)[-1]`; see AC1–AC4 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greeting_words(name)[-1]` | Selected | Reuses the existing split rule and validation, and is exactly the AC4 oracle |
| `greet(name).rsplit(maxsplit=1)[-1]` | Rejected | Duplicates the split rule instead of reusing `greeting_words` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #344 | 2026-11-22 | Initial feature design |
