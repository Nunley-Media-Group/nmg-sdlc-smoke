# Design: Add greeting_json library helper

**Issue**: #368
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Apply `json.dumps` with default arguments to the existing `greet(name)` result, export the helper from the package root, and document it in the README Library section. The change adds one standard-library import (`json`) and no runtime dependency.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`:

- add `import json` immediately after `import html` (alphabetical standard-library imports);
- add this immediately after `greeting_html_escaped` and before `greeting_quoted_printable`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_json(name: str) -> str:
    return json.dumps(greet(name))
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Encoding rule.** `json.dumps` defaults (`ensure_ascii=True`) wrap the string in double quotes, escape `"` as `\"`, `\` as `\\`, control characters as short escapes (`\t`, `\n`, …) or `\u00XX`, and every non-ASCII code point as `\uXXXX` (surrogate pairs above the BMP). The result is ASCII-only and `json.loads` round-trips to `greet(name)`.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_is_title` < `greeting_json` < `greeting_last_word`):

- add `from .greet import greeting_json as greeting_json` immediately after the `greeting_is_title` import;
- add `"greeting_json"` to `__all__` immediately after `"greeting_is_title"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_json,` to the import list immediately after `greeting_is_title,`;
- add the example `greeting_json("Ada")  # '"Hello, Ada"'` immediately after the `greeting_html_escaped("<Ada & Bo>")` example;
- add this exact prose line immediately after the `greeting_html_escaped` prose line:

```markdown
`greeting_json` returns `json.dumps` of the complete greeting (not the name alone), including the `Hello, ` prefix, with default settings, so the result is a JSON string literal with surrounding double quotes in which `"`, `\`, and control characters are escaped and every non-ASCII character becomes a `\uXXXX` escape (for example `Ada` gives `"Hello, Ada"`); decoding it with `json.loads` returns the greeting, and it inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: four independent acceptance scenarios go in `tests/features/add_greeting_json_library_helper.feature`, with steps in `tests/features/steps/test_greeting_json_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_json(name: str) -> str` | Valid nonblank string name | `json.dumps(greet(name))`. Invalid input raises `ValueError("name must not be blank")` | See AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `json.dumps(greet(name))` | Selected | One-line pattern identical to `greeting_html_escaped`; reuses validation; always-ASCII output |
| `json.dumps(greet(name), ensure_ascii=False)` | Rejected | Issue scope requires `\uXXXX` escaping of non-ASCII |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #368 | 2026-11-23 | Initial feature design |
