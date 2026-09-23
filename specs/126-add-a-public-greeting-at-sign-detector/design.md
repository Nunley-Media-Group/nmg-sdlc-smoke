# Design: Add a public greeting at-sign detector

**Issue**: #126
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## Overview

Add a pure helper beside `greeting_has_colon` in `src/nmg_sdlc_smoke/greet.py`, export it from `src/nmg_sdlc_smoke/__init__.py`, and document it with the library helpers in `README.md`. No new module or runtime dependency is needed.

## Architecture

`greeting_has_at_sign(name: str) -> bool` returns `"@" in greet(name)`, querying the completed greeting once and propagating `greet`'s `ValueError("name must not be blank")` for invalid input. Add a package-root import and `__all__` entry; do not change `greet`, existing punctuation helpers, or `src/nmg_sdlc_smoke/cli.py`.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `from nmg_sdlc_smoke import greeting_has_at_sign` | `name: str` | `bool`; invalid input raises `ValueError("name must not be blank")` | `True` exactly when the completed greeting contains literal `@`; otherwise `False`. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #126 | 2026-09-23 | Initial feature design |
