# Design: Add greeting_char_frequency library helper

**Issue**: #329
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG

## Overview

Build the frequency map from `greet(name)` with a plain `dict` and a single pass in order, using only built-ins. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_unique_char_count` and before `greeting_letter_count`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_char_frequency(name: str) -> dict[str, int]:
    frequency: dict[str, int] = {}
    for character in greet(name):
        frequency[character] = frequency.get(character, 0) + 1
    return frequency
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Order.** A `dict` keeps insertion order, so each key appears where its character first occurs.
- **Code points.** Iterating a `str` yields code points, so a decomposed `"e\u0308"` adds to `"e"` and adds a `"\u0308"` key. No normalization runs.
- **Type.** The function returns a fresh built-in `dict`, never a `collections.Counter`, so `type(result) is dict` holds.

In `src/nmg_sdlc_smoke/__init__.py`, keep the existing alphabetical order (`greeting_casefold` < `greeting_char_frequency` < `greeting_codepoints`):

- add `from .greet import greeting_char_frequency as greeting_char_frequency` immediately after the `greeting_casefold` import;
- add `"greeting_char_frequency"` to `__all__` immediately after `"greeting_casefold"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_char_frequency,` to the import list immediately after `greeting_casefold,`;
- add the example `greeting_char_frequency("Ada")  # {"H": 1, "e": 1, "l": 2, "o": 1, ",": 1, " ": 1, "A": 1, "d": 1, "a": 1}` immediately after the `greeting_codepoints("Ada")` example;
- add this exact prose line immediately after the `greeting_codepoints` prose line:

```markdown
`greeting_char_frequency` returns a new plain `dict[str, int]` mapping each character (Unicode code point) of the complete greeting (not the name alone), including the `Hello, ` prefix, comma, and spaces, to the number of times it occurs; keys are case-sensitive and appear in the order each character first occurs (for example `Ada` gives `{"H": 1, "e": 1, "l": 2, "o": 1, ",": 1, " ": 1, "A": 1, "d": 1, "a": 1}`), no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: five independent acceptance scenarios go in `tests/features/add_greeting_char_frequency_library_helper.feature`, with steps in `tests/features/steps/test_greeting_char_frequency_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_char_frequency(name: str) -> dict[str, int]` | Valid nonblank string name | Plain `dict` of code point → positive count. Invalid input raises `ValueError("name must not be blank")` | Case-sensitive, first-seen key order, no normalization; see AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Plain `dict` with a single pass in order | Selected | Gives exactly a `dict` with first-seen order and needs no import |
| `collections.Counter(greet(name))` | Rejected | Returns a `Counter` subclass; issue #329 requires `type(result) is dict` |
| `dict(Counter(...))` | Rejected | Correct, but adds an import for no gain over the loop |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #329 | 2026-11-19 | Initial feature design |
