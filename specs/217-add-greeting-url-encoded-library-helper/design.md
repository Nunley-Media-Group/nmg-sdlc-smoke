# Design: Add greeting_url_encoded library helper

**Issue**: #217
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing encoded-greeting helper pattern (`greeting_sha256`, `greeting_base64`):
1. Call `greet(name)`, which validates the name.
2. Return the standard-library `urllib.parse.quote(..., safe="")` result of the completed greeting.

Export the helper from the package root and document it in the README Library section. No new module, constant, or runtime dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `from urllib.parse import quote` immediately after `from collections.abc import Iterable`;
- add the following immediately after `greeting_base64`, separated from its neighbors by two blank lines:

```python
def greeting_url_encoded(name: str) -> str:
    return quote(greet(name), safe="")
```

- **Validation.** `greet(name)` runs first. Invalid names therefore propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding.** `quote` encodes `str` input as UTF-8 by default and emits uppercase hex digits. With `safe=""`, it leaves only the RFC 3986 unreserved characters (`A`–`Z`, `a`–`z`, `0`–`9`, `-`, `.`, `_`, `~`) unencoded, so `/` is encoded too. Space becomes `%20`, never `+`. It returns a `str`, is pure, and `urllib.parse.unquote` reverses it exactly.

In `src/nmg_sdlc_smoke/__init__.py`:
- add the self-aliased import `from .greet import greeting_url_encoded as greeting_url_encoded` immediately after `from .greet import greeting_starts_with_hello as greeting_starts_with_hello`;
- add `"greeting_url_encoded"` to `__all__` immediately after `"greeting_starts_with_hello"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_url_encoded,` to the import list immediately after `greeting_starts_with_hello,`;
- add the example `greeting_url_encoded("Ada")  # "Hello%2C%20Ada"` as the last line of the first Python block;
- add this exact prose line immediately after the `greeting_base64` prose line:

```markdown
`greeting_url_encoded` percent-encodes the complete greeting (not the name alone) as UTF-8 with uppercase hex digits, leaving only `A`–`Z`, `a`–`z`, `0`–`9`, `-`, `.`, `_`, and `~` unencoded (so a space becomes `%20` and `/` becomes `%2F`); `urllib.parse.unquote` restores the greeting, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- five independent acceptance scenarios go in `tests/features/add_greeting_url_encoded_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_url_encoded_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_url_encoded(name: str) -> str` | Valid nonblank string name | Percent-encoded `str` of the completed greeting. Invalid input raises `ValueError("name must not be blank")` | `"Ada"` → `Hello%2C%20Ada`; `"A/B&C~d_e.f"` → `Hello%2C%20A%2FB%26C~d_e.f`; `"Zoë"` → `Hello%2C%20Zo%C3%AB` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `quote(greet(name), safe="")` | Selected | Standard library; RFC 3986 unreserved set only; one line |
| `quote(greet(name))` with the default `safe="/"` | Rejected | Leaves `/` unencoded, which breaks use as a single path segment |
| `quote_plus` | Rejected | Form encoding turns space into `+`; out of scope |
| `nmg-smoke --url-encoded` flag | Rejected | The issue limits the change to the library; CLI output stays unchanged |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #217 | 2026-10-24 | Initial feature design |
