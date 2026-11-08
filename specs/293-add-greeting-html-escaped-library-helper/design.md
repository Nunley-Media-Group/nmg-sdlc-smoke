# Design: Add greeting_html_escaped library helper

**Issue**: #293
**Date**: 2026-11-08
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/217-add-greeting-url-encoded-library-helper/

## Overview

Follow `greeting_url_encoded`. Call `greet(name)`, which validates the name, then return `html.escape(...)` of the completed greeting with its default `quote=True`. Export the helper from the package root and document it in the README Library section. This adds one standard-library import (`html`) and no new module or runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:
- add `import html` to the standard-library imports, immediately after `import hashlib` and before `import string`;
- add the following immediately after `greeting_url_encoded` and before `greeting_crc32`, separated from its neighbors by two blank lines:

```python
def greeting_html_escaped(name: str) -> str:
    return html.escape(greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Escaping.** `html.escape` with `quote=True` replaces `&` first, then `<`, `>`, `"`, and `'` with `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;`. Every other character, including non-ASCII, passes through unchanged; no Unicode normalization is applied.
- **Return type.** `str`.

In `src/nmg_sdlc_smoke/__init__.py`, keeping the existing alphabetical order:
- add the self-aliased import `from .greet import greeting_html_escaped as greeting_html_escaped` immediately after the `greeting_has_underscore` import, before the `greeting_is_ascii` import;
- add `"greeting_html_escaped"` to `__all__` immediately after `"greeting_has_underscore"`, before `"greeting_is_ascii"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:
- add `greeting_html_escaped,` to the import list immediately after `greeting_has_underscore,`, before `greeting_is_ascii,`;
- add the example `greeting_html_escaped("<Ada & Bo>")  # "Hello, &lt;Ada &amp; Bo&gt;"` immediately after the `greeting_url_encoded("Ada")` example;
- add this exact prose line immediately after the `greeting_url_encoded` prose line:

```markdown
`greeting_html_escaped` escapes the complete greeting (not the name alone), including the `Hello, ` prefix, with `html.escape` and its default `quote=True`, so `&`, `<`, `>`, `"`, and `'` become `&amp;`, `&lt;`, `&gt;`, `&quot;`, and `&#x27;` while every other character, including non-ASCII, is unchanged; it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests:
- unit tests go in `tests/test_greet.py`;
- four independent acceptance scenarios go in `tests/features/add_greeting_html_escaped_library_helper.feature`;
- their steps go in `tests/features/steps/test_greeting_html_escaped_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_html_escaped(name: str) -> str` | Valid nonblank string name | HTML-escaped `str`. Invalid input raises `ValueError("name must not be blank")` | `html.escape(greet(name))`; see AC1 and AC2 for exact results for `"Ada"`, `"Zoë"`, `"<Ada & Bo>"`, and `O'Brien "Jr"` |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `html.escape(greet(name))` | Selected | Standard library; default `quote=True` makes the result safe in text and quoted attribute values |
| `html.escape(greet(name), quote=False)` | Rejected | Out of scope; leaves quotes unescaped in attribute values |
| `xml.sax.saxutils.escape` | Rejected | Does not escape quotes by default; differs from the issue contract |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #293 | 2026-11-08 | Initial feature design |
