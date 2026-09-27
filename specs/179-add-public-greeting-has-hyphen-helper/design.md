# Design: Add public greeting_has_hyphen helper

**Issue**: #179
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Overview

Follow existing literal-character predicates over the completed greeting. Reuse `greet` for validation and export a boolean helper from the package root; no new module or dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add `def greeting_has_hyphen(name: str) -> bool:` beside `greeting_has_underscore`, returning `"-" in greet(name)`. Do not normalize Unicode or separately inspect/validate the name. Add the self-aliased import `from .greet import greeting_has_hyphen as greeting_has_hyphen` and a `"greeting_has_hyphen"` `__all__` entry in `src/nmg_sdlc_smoke/__init__.py` in alphabetical position, preserving existing exports. In `README.md` Library, add `greeting_has_hyphen` to the import block, the examples `greeting_has_hyphen("Mary-Jane")  # True` and `greeting_has_hyphen("Ada")  # False`, and prose stating that only literal `-` (U+002D) in the completed greeting matches (not Unicode dashes such as `‐` or `–`) and invalid names inherit `greet`'s `ValueError("name must not be blank")`. Add focused unit tests in `tests/test_greet.py` and independent AC1–AC4 pytest-bdd scenarios in `tests/features/add_public_greeting_has_hyphen_helper.feature` with steps in `tests/features/steps/test_greeting_has_hyphen_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_hyphen(name: str) -> bool` | Nonblank string name | Python `True`/`False`; invalid input raises `ValueError("name must not be blank")` | Check literal `-` (U+002D) in the unmodified `greet(name)` output; `‐` (U+2010) or `–` (U+2013) alone is not a match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #179 | 2026-09-26 | Initial feature design |
