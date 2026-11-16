# Design: Add greeting_words library helper

**Issue**: #319
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/93-add-greeting-word-count-lifecycle-fixture/

## Overview

Follow `greeting_word_count`. Call `greet(name)`, which validates the name, and return `str.split()` of the completed greeting. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_word_count` and before `greeting_vowel_count`, using the same blank-line spacing as its neighbors:

```python
def greeting_words(name: str) -> list[str]:
    return greet(name).split()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Transform.** `str.split()` with no arguments on the complete greeting, including `Hello, `: splits on runs of any whitespace and never yields empty items. Punctuation is not stripped.
- **Return type.** `str.split()` builds a new `list[str]` on every call.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order (`greeting_word_count` sorts before `greeting_words`):
- add `from .greet import greeting_words as greeting_words` immediately after the `greeting_word_count` import;
- add `"greeting_words"` to `__all__` immediately after `"greeting_word_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_words,` to the import list immediately after `greeting_word_count,`;
- add the example `greeting_words("Ada")  # ['Hello,', 'Ada']` immediately after the `greeting_word_count("Ada Lovelace")  # 3` example;
- add this exact prose line immediately after the `greeting_word_count` prose line:

```markdown
`greeting_words` returns a new `list[str]` of the whitespace-separated words of the complete greeting (not the name alone), using Python's `str.split()` semantics so runs of any whitespace separate words and punctuation stays attached (for example `Ada` gives `['Hello,', 'Ada']`); its length always equals `greeting_word_count`, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_words_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_words_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_words(name: str) -> list[str]` | Valid nonblank string name | `list[str]`. Invalid input raises `ValueError("name must not be blank")` | `greet(name).split()`; see AC1 and AC2 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `str.split()` with no arguments | Selected | Fixed by issue #319; matches `greeting_word_count` |
| `str.split(" ")` | Rejected | Yields empty items for repeated spaces and ignores tabs; diverges from `greeting_word_count` |
| `tuple[str, ...]` | Rejected | Issue #319 fixes the return type as `list[str]` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #319 | 2026-11-15 | Initial feature design |
