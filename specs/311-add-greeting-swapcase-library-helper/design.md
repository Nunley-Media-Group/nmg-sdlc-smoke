# Design: Add greeting_swapcase library helper

**Issue**: #311
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/308-add-greeting-is-title-library-helper/

## Overview

Follow `greeting_casefold`. Call `greet(name)`, which validates the name, and return `str.swapcase()` of the completed greeting. Export the helper from the package root and document it in the README Library section. No new import, module, or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add the following immediately after `greeting_casefold` and before `greeting_reversed`, separated from its neighbors by two blank lines:

```python
def greeting_swapcase(name: str) -> str:
    return greet(name).swapcase()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Transform.** `str.swapcase()` on the complete greeting, including `Hello, `. Uncased characters are unchanged. No Unicode normalization is applied.
- **Return type.** `str`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_swapcase as greeting_swapcase` immediately after the `greeting_starts_with_hello` import and before the `greeting_unique_char_count` import;
- add `"greeting_swapcase"` to `__all__` immediately after `"greeting_starts_with_hello"` and before `"greeting_unique_char_count"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_swapcase,` to the import list immediately after `greeting_starts_with_hello,`;
- add the example `greeting_swapcase("Ada")  # "hELLO, aDA"` immediately after the `greeting_casefold("Straße")  # "hello, strasse"` example;
- add this exact prose line immediately after the `greeting_casefold` prose line:

```markdown
`greeting_swapcase` returns `str.swapcase()` of the complete greeting (not the name alone), including the `Hello, ` prefix, so uppercase characters become lowercase, lowercase characters become uppercase, and uncased characters are unchanged (for example `Ada` gives `hELLO, aDA`); no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- three independent acceptance scenarios go in `tests/features/add_greeting_swapcase_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_swapcase_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_swapcase(name: str) -> str` | Valid nonblank string name | `str`. Invalid input raises `ValueError("name must not be blank")` | `greet(name).swapcase()`; see AC1 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `str.swapcase()` on the complete greeting | Selected | Standard library and deterministic; matches issue #311 and the existing `--swapcase` CLI transform |
| Swapping only the name | Rejected | Out of scope; the issue fixes the complete greeting as the subject |
| Refactoring the CLI to call the new helper | Rejected | The CLI applies swapcase after other transforms; the issue leaves the CLI unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #311 | 2026-11-14 | Initial feature design |
