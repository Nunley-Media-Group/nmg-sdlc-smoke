# Design: Add greeting_slug library helper

**Issue**: #326
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG

## Overview

Derive the slug from `greet(name)` using only the standard library (`unicodedata`, `re`). Export the helper from the package root and document it in the README Library section. No new module or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:

- Add `import re` immediately after `import quopri` and `import unicodedata` immediately after `import string`, keeping the import block sorted (Ruff clean).
- Add the following immediately after `greeting_reversed` and before `greeting_word_count`, using the same blank-line spacing as its neighbors:

```python
def greeting_slug(name: str) -> str:
    decomposed = unicodedata.normalize("NFKD", greet(name))
    ascii_base = "".join(
        char for char in decomposed if not unicodedata.combining(char)
    )
    return re.sub(r"[^a-z0-9]+", "-", ascii_base.lower()).strip("-")
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Transliteration.** NFKD splits `ë` into `e` + U+0308 and folds fullwidth `Ａ` to `A`; dropping combining marks leaves the ASCII base.
- **Separators.** Anything still outside `[a-z0-9]` after lowercasing (spaces, tabs, punctuation, `_`, `李`) joins one run and becomes a single `-`; `strip("-")` removes edge hyphens. `Hello` guarantees a non-empty result.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order (`greeting_shake_256` < `greeting_slug` < `greeting_space_count`):

- add `from .greet import greeting_slug as greeting_slug` immediately after the `greeting_shake_256` import;
- add `"greeting_slug"` to `__all__` immediately after `"greeting_shake_256"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_slug,` to the import list immediately after `greeting_shake_256,`;
- add the example `greeting_slug("Ada Lovelace")  # "hello-ada-lovelace"` immediately after the `greeting_reversed("Ada")  # "adA ,olleH"` example;
- add this exact prose line immediately after the `greeting_reversed` prose line:

```markdown
`greeting_slug` returns a lowercase ASCII slug of the complete greeting (not the name alone): it applies Unicode NFKD normalization and drops combining marks (so `Zoë` gives `hello-zoe`), lowercases, replaces every run of characters other than `a`–`z` and `0`–`9` with a single `-`, and trims leading and trailing `-` (for example `Ada Lovelace` gives `hello-ada-lovelace`); characters with no ASCII base, such as `李`, act as separators, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: five independent acceptance scenarios go in `tests/features/add_greeting_slug_library_helper.feature`, with steps in `tests/features/steps/test_greeting_slug_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_slug(name: str) -> str` | Valid nonblank string name | `str` matching `^[a-z0-9]+(-[a-z0-9]+)*$`. Invalid input raises `ValueError("name must not be blank")` | NFKD + drop combining marks, lowercase, `[^a-z0-9]+` → `-`, strip edge `-`; see AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| NFKD transliteration, non-ASCII leftovers as separators | Selected | Fixed by issue #326 |
| `encode("ascii", "ignore")` after NFKD | Rejected | Drops `李` instead of separating, so `Ada李Lee` would give `hello-adalee` |
| Keep Unicode letters | Rejected | Issue #326 requires an ASCII-only slug |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #326 | 2026-11-19 | Initial feature design |
