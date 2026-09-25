# Design: Add public greeting_has_asterisk helper

**Issue**: #155
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/152-add-public-greeting-has-backtick-library-helper/

## Overview

Implement an exact-character query on the completed greeting using the existing simple punctuation-helper pattern. Delegate invalid-input handling to `greet`; leave the CLI and greeting formatting unchanged.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, add `def greeting_has_asterisk(name: str) -> bool:` returning `"*" in greet(name)`. This compares U+002A against the completed greeting and leaves U+2217 distinct. Explicitly import the function in `src/nmg_sdlc_smoke/__init__.py` and add it to `__all__`, retaining every existing export. Document the public import, positive, negative, lookalike, and inherited-validation examples in `README.md`'s Library section. `src/nmg_sdlc_smoke/cli.py` continues calling `greet` directly.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_asterisk(name: str) -> bool` | Nonblank string name | Python `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Return `True` only when completed `greet(name)` contains literal U+002A; U+2217 does not match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #155 | 2026-09-24 | Initial feature design |
