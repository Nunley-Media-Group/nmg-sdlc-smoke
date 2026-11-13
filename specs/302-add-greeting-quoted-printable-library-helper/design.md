# Design: Add greeting_quoted_printable library helper

**Issue**: #302
**Date**: 2026-11-13
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/293-add-greeting-html-escaped-library-helper/

## Overview

Follow `greeting_html_escaped`. Call `greet(name)`, which validates the name, encode the completed greeting as UTF-8, pass the bytes to `quopri.encodestring` with its defaults, and decode the result as ASCII. Export the helper from the package root and document it in the README Library section. The only new import is the standard library `quopri` module; no new module or runtime dependency is added.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import quopri` to the standard library import block in alphabetical order, immediately after `import html` and before `import string`;
- add the following immediately after `greeting_html_escaped` and before `greeting_crc32`, separated from its neighbors by two blank lines:

```python
def greeting_quoted_printable(name: str) -> str:
    return quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** UTF-8 of the complete greeting, including `Hello, `; `quopri.encodestring` defaults (`quotetabs=False`, `header=False`); no Unicode normalization.
- **Return type.** `str` (quoted-printable output is pure ASCII).

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add `from .greet import greeting_quoted_printable as greeting_quoted_printable` immediately after the `greeting_punctuation_count` import, before the `greeting_reversed` import;
- add `"greeting_quoted_printable"` to `__all__` immediately after `"greeting_punctuation_count"`, before `"greeting_reversed"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_quoted_printable,` to the import list immediately after `greeting_punctuation_count,`;
- add the example `greeting_quoted_printable("Zoë")  # "Hello, Zo=C3=AB"` immediately after the `greeting_html_escaped("<Ada & Bo>")` example;
- add this exact prose line immediately after the `greeting_html_escaped` prose line:

```markdown
`greeting_quoted_printable` encodes the complete greeting (not the name alone), including the `Hello, ` prefix, as UTF-8 and returns its quoted-printable form from `quopri.encodestring` with default options as an ASCII `str`, so `=` and non-ASCII bytes become `=XX` escapes with uppercase hex digits and trailing whitespace is escaped while other printable ASCII is unchanged; no Unicode normalization is applied, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- three independent acceptance scenarios go in `tests/features/add_greeting_quoted_printable_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_quoted_printable_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_quoted_printable(name: str) -> str` | Valid nonblank string name | ASCII `str`. Invalid input raises `ValueError("name must not be blank")` | `quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")`; see AC1 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `quopri.encodestring` with defaults | Selected | Standard library, deterministic, matches issue #302 |
| `quotetabs=True` or `header=True` | Rejected | Out of scope; changes space handling the issue fixes |
| `binascii.b2a_qp` directly | Rejected | Issue #302 fixes the oracle as `quopri.encodestring` |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #302 | 2026-11-13 | Initial feature design |
