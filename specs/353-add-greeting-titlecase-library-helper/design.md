# Design: Add greeting_titlecase library helper

**Issue**: #353
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Overview

Apply `str.title()` to the existing `greet(name)` result. Export the helper from the package root and document it in the README Library section. The change adds no import, module, or runtime dependency, and leaves the CLI unchanged.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add this immediately after `greeting_swapcase` and before `greeting_nfc`, with the same two-blank-line spacing as its neighbors:

```python
def greeting_titlecase(name: str) -> str:
    return greet(name).title()
```

- **Validation.** `greet(name)` runs first, so invalid names propagate its `ValueError("name must not be blank")` unchanged.
- **Casing.** `str.title()` uppercases the first letter of each run of letters and lowercases the rest; a letter after a digit or apostrophe starts a new run (`o'brien` → `O'Brien`, `007x` → `007X`). Whitespace and non-letters are unchanged; no normalization is applied.
- **CLI agreement.** `src/nmg_sdlc_smoke/cli.py` applies `message.title()` to `greet(name)` for `--titlecase`, so for a plain invocation the CLI prints `greeting_titlecase(name)` followed by a newline. The CLI is not modified.

In `src/nmg_sdlc_smoke/__init__.py`, keep alphabetical order (`greeting_swapcase` < `greeting_titlecase` < `greeting_unique_char_count`):

- add `from .greet import greeting_titlecase as greeting_titlecase` immediately after the `greeting_swapcase` import;
- add `"greeting_titlecase"` to `__all__` immediately after `"greeting_swapcase"`;
- keep every existing import and `__all__` entry.

In the `README.md` `## Library` section:

- add `greeting_titlecase,` to the import list immediately after `greeting_swapcase,`;
- add the example `greeting_titlecase("ada lovelace")  # "Hello, Ada Lovelace"` immediately after the `greeting_swapcase("Ada")  # "hELLO, aDA"` example;
- add this exact prose line immediately after the `greeting_swapcase` prose line:

```markdown
`greeting_titlecase` returns `str.title()` of the complete greeting (not the name alone), including the `Hello, ` prefix, so each run of letters starts with an uppercase character followed by lowercase characters, and a letter after a digit or apostrophe also starts a new run (for example `ada lovelace` gives `Hello, Ada Lovelace` and `o'brien` gives `Hello, O'Brien`); it matches `nmg-smoke --titlecase` output without the trailing newline, applies no Unicode normalization, and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names.
```

Tests: five independent acceptance scenarios go in `tests/features/add_greeting_titlecase_library_helper.feature`, with steps in `tests/features/steps/test_greeting_titlecase_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_titlecase(name: str) -> str` | Valid nonblank string name | Title-cased greeting. Invalid input raises `ValueError("name must not be blank")` | Equals `greet(name).title()`; see AC1–AC3 for exact results |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| `greet(name).title()` | Selected | Matches the CLI `--titlecase` behavior exactly and is the AC3 oracle |
| `string.capwords(greet(name))` | Rejected | Differs from `str.title()` after apostrophes and digits and would diverge from the CLI |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #353 | 2026-11-23 | Initial feature design |
