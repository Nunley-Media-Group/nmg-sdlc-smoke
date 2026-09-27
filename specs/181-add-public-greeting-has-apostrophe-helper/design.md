# Design: Add public greeting_has_apostrophe helper

**Issue**: #181
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/171-add-public-greeting-has-double-quote-helper/

## Overview

Follow the existing literal-character predicates over the completed greeting. Reuse `greet` for validation and export a boolean helper from the package root; no new module or dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add `def greeting_has_apostrophe(name: str) -> bool:` after `greeting_has_slash`, returning `"'" in greet(name)`. Do not normalize Unicode, transform the name, or validate the name separately; `greet` raises `ValueError("name must not be blank")` for invalid input. In `src/nmg_sdlc_smoke/__init__.py`, add `from .greet import greeting_has_apostrophe as greeting_has_apostrophe` and the `"greeting_has_apostrophe"` `__all__` entry, both immediately before the `greeting_has_ascii_asterisk` lines to keep alphabetical order, preserving every existing export. In `README.md` Library, add `greeting_has_apostrophe,` to the import block before `greeting_has_ascii_asterisk,`; add the examples `greeting_has_apostrophe("O'Brien")  # True`, `greeting_has_apostrophe("Ada")  # False`, and `greeting_has_apostrophe("O’Brien")  # False` before the `greeting_has_ascii_asterisk` examples; and append after the `greeting_has_slash` prose line: `` `greeting_has_apostrophe` checks for a literal ASCII `'` (U+0027) in the completed greeting (not `’` U+2019, `ʼ` U+02BC, or `` ` `` U+0060) and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. ``

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_apostrophe(name: str) -> bool` | Nonblank string name | Python `True`/`False`; invalid input raises `ValueError("name must not be blank")` | Check literal `'` (U+0027) in the unmodified `greet(name)` output; U+2019, U+2018, U+02BC, U+0060, and U+2032 alone are not matches. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #181 | 2026-09-27 | Initial feature design |
