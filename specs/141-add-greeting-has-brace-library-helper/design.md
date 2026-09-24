# Design: Add greeting_has_brace library helper

**Issue**: #141
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Overview

Add a pure typed predicate for the literal opening brace in the completed greeting. Use `greet(name)` to centralize formatting and invalid-name handling.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add `def greeting_has_brace(name: str) -> bool:` beside the punctuation predicates, returning `"{" in greet(name)`. Re-export it and add it to `__all__` in `src/nmg_sdlc_smoke/__init__.py`, retaining every existing export. Add focused cases in `tests/test_greet.py` and four AC-linked scenarios with pytest-bdd steps under `tests/features/`. The library does not call the CLI.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_brace(name: str) -> bool` | Valid nonblank string name | `True` or `False`; invalid name raises `ValueError("name must not be blank")` | Return literal `{` membership of the complete `greet(name)`; `}` alone does not match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #141 | 2026-09-24 | Initial feature design |
