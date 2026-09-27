# Design: Add public greeting_has_backslash helper

**Issue**: #185
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing literal-character predicate pattern over the completed greeting (for example `greeting_has_slash`). Reuse `greet` for input validation and export a boolean predicate from the package root; no new module or dependency is needed.

## Architecture

Add `def greeting_has_backslash(name: str) -> bool:` in `src/nmg_sdlc_smoke/greet.py` immediately after `greeting_has_slash`, returning `"\\" in greet(name)`. Calling `greet` first means invalid names raise `greet`'s `ValueError("name must not be blank")` unchanged, and the check inspects the completed greeting's actual characters with no Unicode normalization or escape processing, so only U+005C matches.

In `src/nmg_sdlc_smoke/__init__.py`, add the self-aliased import `from .greet import greeting_has_backslash as greeting_has_backslash` and the `__all__` entry `"greeting_has_backslash"`, each placed alphabetically immediately before the `greeting_has_backtick` line; retain all existing exports.

In the `README.md` Library section, add `greeting_has_backslash,` to the import list immediately before `greeting_has_backtick,`; add the examples `greeting_has_backslash("Ada\\")  # True` and `greeting_has_backslash("Ada")  # False` immediately before the first `greeting_has_backtick` example; and add, immediately after the `greeting_has_backtick` prose line, the sentence: `` `greeting_has_backslash` matches only a literal ASCII backslash `\` (U+005C) in the completed greeting, not `/` (U+002F), the fullwidth `＼` (U+FF3C), or `∖` (U+2216), and inherits `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. ``

Unit tests go in `tests/test_greet.py`; four independent acceptance scenarios go in `tests/features/add_public_greeting_has_backslash_helper.feature` with steps in `tests/features/steps/test_greeting_has_backslash_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_backslash(name: str) -> bool` | Valid nonblank string name | `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Query literal `\` (U+005C) in unmodified `greet(name)` output; `/`, `＼`, and `∖` alone are not matches. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #185 | 2026-09-27 | Initial feature design |
