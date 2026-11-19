# Design: Add greeting_initials library helper

**Issue**: #323
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/319-add-greeting-words-library-helper/

## Overview

Build on `greeting_words`. Call `greeting_words(name)`, which validates the name through `greet` and splits the completed greeting with `str.split()`. Then join the first character of each word. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_words` and before `greeting_vowel_count`, using the same blank-line spacing as its neighbors:

```python
def greeting_initials(name: str) -> str:
    return "".join(word[0] for word in greeting_words(name))
```

- **Validation.** `greet(name)` runs first inside `greeting_words`, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Transform.** `str.split()` never yields empty items, so `word[0]` is always defined. Characters are taken as-is: no case change, no punctuation skipping, no separator.
- **Length.** One character per word, so the result length equals `greeting_word_count(name)`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order (`greeting_html_escaped` < `greeting_initials` < `greeting_is_ascii`):
- add `from .greet import greeting_initials as greeting_initials` immediately after the `greeting_html_escaped` import;
- add `"greeting_initials"` to `__all__` immediately after `"greeting_html_escaped"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_initials,` to the import list immediately after `greeting_html_escaped,`;
- add the example `greeting_initials("Ada Lovelace")  # "HAL"` immediately after the `greeting_words("Ada")  # ['Hello,', 'Ada']` example;
- add this exact prose line immediately after the `greeting_words` prose line:

```markdown
`greeting_initials` returns a `str` made of the first character of each whitespace-separated word of the complete greeting (not the name alone), using the same `str.split()` words as `greeting_words` with the original case preserved and no separator (for example `Ada Lovelace` gives `HAL` and `ada lovelace` gives `Hal`); its length always equals `greeting_word_count`, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_initials_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_initials_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_initials(name: str) -> str` | Valid nonblank string name | `str`. Invalid input raises `ValueError("name must not be blank")` | `"".join(word[0] for word in greet(name).split())`; see AC1 and AC2 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Reuse `greeting_words` and preserve case | Selected | Fixed by issue #323; keeps one splitting rule |
| Uppercase the initials | Rejected | Issue #323 requires case preservation (`ada lovelace` gives `Hal`) |
| Skip leading punctuation in words | Rejected | Out of scope in issue #323 |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #323 | 2026-11-19 | Initial feature design |
