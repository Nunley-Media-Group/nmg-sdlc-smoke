# Design: Add greeting_is_title library helper

**Issue**: #308
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/305-add-greeting-is-printable-library-helper/

## Overview

Follow `greeting_is_printable`. Call `greet(name)`, which validates the name, and return `str.istitle()` of the completed greeting. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_is_printable` and before `greeting_starts_with_hello`, separated from its neighbors by two blank lines:

```python
def greeting_is_title(name: str) -> bool:
    return greet(name).istitle()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Check.** `str.istitle()` on the complete greeting, including `Hello, `. An uppercase or titlecase character may follow only an uncased character, and a lowercase character only a cased one. At least one cased character is required, and the `Hello` prefix always supplies one. For example, the apostrophe in `O'Neil` is uncased, so `N` may be uppercase, while the `A` in `McAdam` follows the cased `c`, so the result is `False`. No Unicode normalization is applied.
- **Return type.** `bool`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_is_title as greeting_is_title` immediately after the `greeting_is_printable` import and before the `greeting_length` import;
- add `"greeting_is_title"` to `__all__` immediately after `"greeting_is_printable"` and before `"greeting_length"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_is_title,` to the import list immediately after `greeting_is_printable,`;
- add the examples `greeting_is_title("Ada")  # True` and `greeting_is_title("ada")  # False` immediately after the `greeting_is_printable("Ada\tLovelace")  # False` example;
- add this exact prose line immediately after the `greeting_is_printable` prose line:

```markdown
`greeting_is_title` returns `str.istitle()` of the complete greeting (not the name alone), including the `Hello, ` prefix, so it is `True` when every cased word starts with an uppercase character followed only by lowercase characters (for example `Ada`, `Ada Lovelace`, or `O'Neil`) and `False` otherwise (for example `ada`, `ADA`, or `McAdam`); no case conversion or Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_is_title_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_is_title_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_is_title(name: str) -> bool` | Valid nonblank string name | `bool`. Invalid input raises `ValueError("name must not be blank")` | `greet(name).istitle()`; see AC1 and AC2 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `str.istitle()` on the complete greeting | Selected | Standard library and deterministic; matches issue #308 |
| Checking only the name | Rejected | Out of scope; the issue fixes the complete greeting as the subject |
| Comparing against `greet(name).title()` | Rejected | `title()` rewrites `O'Neil` to `O'Neil` but `McAdam` to `Mcadam`, so its edge cases differ from the `istitle()` oracle the issue fixes |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #308 | 2026-11-14 | Initial feature design |
