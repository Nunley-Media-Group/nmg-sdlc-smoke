# Design: Add public greeting_has_double_quote helper

**Issue**: #171
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Overview

Follow existing literal-character predicates over the completed greeting. Reuse `greet` for validation and export a boolean helper from the package root; no new module or dependency is needed.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add `def greeting_has_double_quote(name: str) -> bool:` beside `greeting_has_dollar`, returning `'"' in greet(name)`. Do not normalize Unicode, inspect the CLI's `--quotes` output, or separately validate the name. Add a self-aliased import and `__all__` entry in `src/nmg_sdlc_smoke/__init__.py`, preserving existing exports. In `README.md` Library, add the import, `greeting_has_double_quote('Ada"')  # True`, `greeting_has_double_quote("Ada")  # False`, and prose stating that only literal `"` in the completed greeting matches and invalid names inherit `greet`'s `ValueError("name must not be blank")`. Add focused unit tests in `tests/test_greet.py` and independent AC1–AC4 pytest-bdd scenarios in `tests/features/add_public_greeting_has_double_quote_helper.feature`, implemented by `tests/features/steps/test_greeting_has_double_quote_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_double_quote(name: str) -> bool` | Nonblank string name | Python `True`/`False`; invalid input raises `ValueError("name must not be blank")` | Check literal `"` (U+0022) in the unmodified `greet(name)` output; fullwidth `＂` (U+FF02) alone is not a match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #171 | 2026-09-26 | Initial feature design |
