# Design: Add greeting_first_word library helper

**Issue**: #379
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Overview

Return the first element of the existing `greeting_words(name)` list. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately before `greeting_last_word` (after `greeting_average_word_length`), with the same two-blank-line spacing as its neighbors:

```python
def greeting_first_word(name: str) -> str:
    return greeting_words(name)[0]
```

- **Validation.** `greeting_words` calls `greet(name)` first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Splitting.** `greeting_words` uses `str.split()` with no arguments. The list always starts with `Hello,`, so `[0]` never raises `IndexError`.
- **Unchanged word.** The word is returned exactly as split, with the comma kept.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_ends_with_name` < `greeting_first_word` < `greeting_has_apostrophe`):

- add `from .greet import greeting_first_word as greeting_first_word` immediately after the `greeting_ends_with_name` import;
- add `"greeting_first_word"` to `__all__` immediately after `"greeting_ends_with_name"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_first_word,` to the import list immediately after `greeting_ends_with_name,`;
- add the example `greeting_first_word("Ada Lovelace")  # 'Hello,'` immediately before the `greeting_last_word("Ada Lovelace")  # 'Lovelace'` example;
- add this exact prose line immediately before the `greeting_last_word` prose line:

```markdown
`greeting_first_word` returns the first whitespace-separated word of the complete greeting (not the name alone) as a `str`, using the same `str.split()` words as `greeting_words` and returning that word unchanged with the comma attached and no case change or Unicode normalization (so every valid name gives `Hello,`), and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: five independent acceptance scenarios go in `tests/features/add_greeting_first_word_library_helper.feature`, with steps in `tests/features/steps/test_greeting_first_word_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_first_word(name: str) -> str` | Valid nonblank string name | First `str.split()` word of the greeting (`"Hello,"`). Invalid input raises `ValueError("name must not be blank")` | Equals `greeting_words(name)[0]`; see AC1–AC3 |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greeting_words(name)[0]` | Selected | Reuses the existing split rule and validation, and is exactly the AC3 oracle |
| Return the literal `"Hello,"` after `greet(name)` | Rejected | Would silently diverge if the greeting format changed |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #379 | 2026-11-25 | Initial feature design |
