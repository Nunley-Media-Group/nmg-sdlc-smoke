# Design: Add greeting_is_printable library helper

**Issue**: #305
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/57-add-greeting-is-ascii-library-function/

## Overview

Follow `greeting_is_ascii`. Call `greet(name)`, which validates the name, and return `str.isprintable()` of the completed greeting. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_is_ascii` and before `greeting_starts_with_hello`, separated from its neighbors by two blank lines:

```python
def greeting_is_printable(name: str) -> bool:
    return greet(name).isprintable()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Check.** `str.isprintable()` on the complete greeting, including `Hello, `. The ASCII space is printable, while tab, newline, and other characters in Unicode categories Cc, Cf, Cs, Co, Cn, Zl, Zp, and Zs (except the ASCII space) are not. No Unicode normalization is applied.
- **Return type.** `bool`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_is_printable as greeting_is_printable` immediately after the `greeting_is_ascii` import and before the `greeting_length` import;
- add `"greeting_is_printable"` to `__all__` immediately after `"greeting_is_ascii"` and before `"greeting_length"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_is_printable,` to the import list immediately after `greeting_is_ascii,`;
- add the examples `greeting_is_printable("Ada")  # True` and `greeting_is_printable("Ada\tLovelace")  # False` immediately after the `greeting_is_ascii("Ada")  # True` example;
- add this exact prose line immediately after the `` `greet` rejects blank, whitespace-only, and non-string names `` prose line:

```markdown
`greeting_is_printable` returns `str.isprintable()` of the complete greeting (not the name alone), including the `Hello, ` prefix, so it is `True` when every character is printable (the ASCII space counts as printable) and `False` when any character, such as a tab or newline, is not; no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_is_printable_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_is_printable_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_is_printable(name: str) -> bool` | Valid nonblank string name | `bool`. Invalid input raises `ValueError("name must not be blank")` | `greet(name).isprintable()`; see AC1 and AC2 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `str.isprintable()` on the complete greeting | Selected | Standard library and deterministic; matches issue #305 |
| Checking only the name | Rejected | Out of scope; the issue fixes the complete greeting as the subject |
| A custom printable character set | Rejected | Issue #305 fixes the oracle as `str.isprintable()` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #305 | 2026-11-14 | Initial feature design |
