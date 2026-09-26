# Design: Add public greeting_has_exclamation helper

**Issue**: #161
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing punctuation predicates over the completed greeting. Reuse `greet` to preserve validation, then export the boolean helper alongside the existing package API without adding a module or dependency.

## Architecture

Add `def greeting_has_exclamation(name: str) -> bool:` in `src/nmg_sdlc_smoke/greet.py` beside the other punctuation queries, returning `"!" in greet(name)`. Do not call `greeting_ends_with_exclamation`, which would append punctuation and give the wrong answer for `Ada`. In `src/nmg_sdlc_smoke/__init__.py`, add the explicit self-aliased import and the `__all__` member, preserving prior entries. In `README.md` Library, add the import, `greeting_has_exclamation("Ada!")  # True`, `greeting_has_exclamation("Ada")  # False`, and a sentence describing literal `!` matching and inherited `ValueError("name must not be blank")`. Focused unit coverage goes in `tests/test_greet.py`; the four scenarios have an executable copy in `tests/features/add_public_greeting_has_exclamation_helper.feature` with steps in `tests/features/steps/test_greeting_has_exclamation_steps.py`, following the existing punctuation-helper feature/step pattern.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_exclamation(name: str) -> bool` | Valid nonblank string name | `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Query literal `!` in the unmodified complete `greet(name)` output; fullwidth `！` alone is not a match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #161 | 2026-09-26 | Initial feature design |
