# Design: Add public greeting_has_hash helper

**Issue**: #138
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Overview

Add a pure typed literal-hash predicate to the existing greeting library. The value comes from the completed `greet(name)` string, so greeting formatting and validation remain centralized.

## Architecture

Add `def greeting_has_hash(name: str) -> bool:` beside the existing punctuation predicates in `src/nmg_sdlc_smoke/greet.py`, returning `"#" in greet(name)`. Re-export the symbol and add it to `__all__` in `src/nmg_sdlc_smoke/__init__.py`. Do not add a CLI path or runtime dependency. Add focused tests in `tests/test_greet.py` and a four-scenario pytest-bdd feature plus steps under `tests/features/`. In `README.md`'s Library section, add the import and examples for both boolean outcomes.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_hash(name: str) -> bool` | A nonblank string name | `True` or `False`; invalid name raises `ValueError("name must not be blank")` | Return whether the complete `greet(name)` contains literal `#`, without transforming the greeting. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #138 | 2026-09-24 | Initial feature design |
