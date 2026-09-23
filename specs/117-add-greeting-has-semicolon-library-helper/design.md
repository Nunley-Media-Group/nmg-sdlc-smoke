# Design: Add greeting_has_semicolon library helper

**Issue**: #117
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## Overview

Add a pure typed helper alongside the existing derived helpers in `src/nmg_sdlc_smoke/greet.py`. Evaluate `";" in greet(name)`, rather than checking an unchecked input or duplicating validation, and export the function from the package root. The default greeting and CLI are not modified.

## Architecture

`greet(name)` constructs and validates the greeting once. `greeting_has_semicolon(name: str) -> bool` returns the membership test on that completed string, so invalid input propagates the same `ValueError("name must not be blank")`. `src/nmg_sdlc_smoke/__init__.py` imports the helper and adds its name to `__all__` without removing existing exports. No new module or runtime dependency is needed: `greeting_is_ascii`, `greeting_starts_with_hello`, and other helpers already follow the `greet(name)` delegation pattern.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `from nmg_sdlc_smoke import greeting_has_semicolon` | `name: str` | `bool`; invalid input raises `ValueError("name must not be blank")` | `True` exactly when literal `;` occurs in complete `greet(name)` text. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #117 | 2026-09-22 | Initial feature design |
