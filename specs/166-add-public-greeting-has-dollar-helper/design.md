# Design: Add public greeting_has_dollar helper

**Issue**: #166
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing punctuation-query pattern over the completed greeting. Reuse `greet` for input validation and export a boolean predicate from the package root; no new module or dependency is needed.

## Architecture

Add `def greeting_has_dollar(name: str) -> bool:` alongside the punctuation helpers in `src/nmg_sdlc_smoke/greet.py`, returning `"$" in greet(name)`. This evaluates the completed greeting rather than separately validating or searching `name`. Add the self-aliased import and `__all__` member in `src/nmg_sdlc_smoke/__init__.py`, retaining existing exports. In `README.md` Library, add the public import, `greeting_has_dollar("Ada$")  # True`, `greeting_has_dollar("Ada")  # False`, and a sentence that literal `$` in the complete greeting is checked and invalid names inherit `greet`'s `ValueError("name must not be blank")`. Focused unit tests go in `tests/test_greet.py`; four independent acceptance scenarios go in `tests/features/add_public_greeting_has_dollar_helper.feature` with step implementations in `tests/features/steps/test_greeting_has_dollar_steps.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_dollar(name: str) -> bool` | Valid nonblank string name | `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Query literal `$` in unmodified `greet(name)` output; fullwidth `＄` alone is not a match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #166 | 2026-09-26 | Initial feature design |
