# Design: Add public greeting_has_plus library helper

**Issue**: #144
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Overview

Add a pure typed literal-plus predicate to the greeting library, inspecting the completed `greet(name)` result so formatting and validation remain centralized.

## Architecture

Add `def greeting_has_plus(name: str) -> bool:` beside `greeting_has_hash` in `src/nmg_sdlc_smoke/greet.py`, returning `"+" in greet(name)`. Re-export it and add it to `__all__` in `src/nmg_sdlc_smoke/__init__.py` without removing or changing prior exports. Add focused tests in `tests/test_greet.py` and four AC-linked pytest-bdd scenarios and steps under `tests/features/`. No new dependency, CLI adapter, or separate validation path.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_plus(name: str) -> bool` | A nonblank string name | `True` or `False`; invalid name raises `ValueError("name must not be blank")` | Return whether the complete `greet(name)` contains literal `+`, without changing its text. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #144 | 2026-09-24 | Initial feature design |
