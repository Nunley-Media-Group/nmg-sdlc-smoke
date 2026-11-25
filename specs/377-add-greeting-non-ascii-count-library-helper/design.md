# Design: Add greeting_non_ascii_count library helper

**Issue**: #377
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## Overview

Count the code points above U+007F in the existing `greet(name)` result, export the helper from the package root, and document it in the README Library section. The change adds no import, module, or runtime dependency, and the CLI stays unchanged.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_letter_count` and before `greeting_sha256`, with the same two-blank-line spacing as the functions around it:

```python
def greeting_non_ascii_count(name: str) -> int:
    return sum(ord(character) > 127 for character in greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names raise its `ValueError("name must not be blank")` unchanged.
- **Counting rule.** Iterating a Python `str` yields code points, so combining marks and astral characters each count once; no normalization is applied. `sum` over booleans returns an `int` (0 when nothing matches).

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_nfkd` < `greeting_non_ascii_count` < `greeting_punctuation_count`):

- add `from .greet import greeting_non_ascii_count as greeting_non_ascii_count` immediately after the `greeting_nfkd` import;
- add `"greeting_non_ascii_count"` to `__all__` immediately after `"greeting_nfkd"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_non_ascii_count,` to the import list immediately after `greeting_nfkd,`;
- add the example `greeting_non_ascii_count("Zo\u00eb")  # 1` immediately after the `greeting_letter_count("Ada")  # 8` example;
- add this exact prose line immediately after the `greeting_letter_count` prose line:

```markdown
`greeting_non_ascii_count` counts the Unicode code points above U+007F in the complete greeting (not the name alone), so `Ada` gives `0` and `Zoë` gives `1`; it counts code points rather than UTF-8 bytes or grapheme clusters and applies no Unicode normalization, so `Zoe` plus U+0308 also gives `1`, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: four independent acceptance scenarios go in `tests/features/add_greeting_non_ascii_count_library_helper.feature`, with steps in `tests/features/steps/test_greeting_non_ascii_count_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_non_ascii_count(name: str) -> int` | Valid nonblank string name | Count of code points in `greet(name)` with `ord > 127`. Invalid input raises `ValueError("name must not be blank")` | See AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `sum(ord(c) > 127 for c in greet(name))` | Selected | Same generator-sum pattern as `greeting_uppercase_count` and `greeting_letter_count`; reuses validation |
| `len(greet(name)) - len(greet(name).encode("ascii", "ignore"))` | Rejected | Equivalent result but indirect and encodes twice |
| `not c.isascii()` per character | Rejected | Equivalent; the explicit `> 127` matches the documented U+007F boundary |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #377 | 2026-11-25 | Initial feature design |
