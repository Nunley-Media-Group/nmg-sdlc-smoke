# Design: Add greeting_has_colon library helper

**Issue**: #120
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## Overview

Add a pure helper next to `greeting_has_semicolon` in `src/nmg_sdlc_smoke/greet.py`; query literal `:` membership in `greet(name)` instead of bypassing its validation. Export the helper from the package root and document it alongside existing helpers. No new module or runtime dependency is needed.

## Architecture

`greeting_has_colon(name: str) -> bool` returns `":" in greet(name)`. This constructs the completed greeting once and propagates `greet`'s `ValueError("name must not be blank")` for invalid input. `src/nmg_sdlc_smoke/__init__.py` adds an import and `__all__` entry without removing existing exports; the CLI and `greet` remain unchanged.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `from nmg_sdlc_smoke import greeting_has_colon` | `name: str` | `bool`; invalid input raises `ValueError("name must not be blank")` | `True` exactly when the complete greeting contains literal ASCII `:`; otherwise `False`. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #120 | 2026-09-22 | Initial feature design |
