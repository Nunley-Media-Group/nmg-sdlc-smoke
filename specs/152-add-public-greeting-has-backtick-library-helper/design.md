# Design: Add public greeting_has_backtick library helper

**Issue**: #152
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Overview

Implement an exact-character query over the completed greeting using the same simple punctuation-helper pattern as `greeting_has_equal`. Delegate invalid-input handling to `greet`; keep the CLI and greeting formatting unchanged.

## Architecture

Add `def greeting_has_backtick(name: str) -> bool:` to `src/nmg_sdlc_smoke/greet.py`, returning whether a literal U+0060 backtick occurs in `greet(name)` via Python substring membership. Do not normalize the greeting or inspect a transformed name. Import the function explicitly into `src/nmg_sdlc_smoke/__init__.py` and add it to `__all__` without removing existing exports. In `README.md`'s Library section, document the new import, `True` for "Ada`", `False` for `Ada` and `Ada｀`, and inherited validation. The existing `cli.py` continues to call `greet` directly.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_backtick(name: str) -> bool` | Nonblank string name | Python `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Return `True` only when the complete greeting contains literal ASCII U+0060; U+FF40 is not a match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #152 | 2026-09-24 | Initial feature design |
