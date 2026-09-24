# Design: Add greeting_has_pipe library helper for verified smoke

**Issue**: #129
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## Overview
Add a pure helper beside the punctuation queries in `src/nmg_sdlc_smoke/greet.py`, export it in `src/nmg_sdlc_smoke/__init__.py`, and document public use in `README.md`. No new module or dependency.

## Architecture
`greeting_has_pipe(name: str) -> bool` returns `"|" in greet(name)`, evaluating the completed greeting once and propagating `greet`'s `ValueError("name must not be blank")` for invalid input. Existing helpers, CLI behavior and greeting formatting remain unchanged.

## Verification
Unit and pytest-bdd scenarios independently cover `True`, `False`, and invalid input. The registered nmg-sdlc smoke provider must prove issue #129 closed by an exact-head merged PR from its invocation; static status or an edited success marker is insufficient.
