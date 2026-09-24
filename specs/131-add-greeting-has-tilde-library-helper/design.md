# Design: Add greeting_has_tilde library helper for review smoke

**Issue**: #131
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Overview
Add one pure helper next to punctuation queries in `src/nmg_sdlc_smoke/greet.py`, export it in `src/nmg_sdlc_smoke/__init__.py`, and document public use in `README.md`. No new module or dependency.

## Architecture
`greeting_has_tilde(name: str) -> bool` returns `"~" in greet(name)`, evaluating the completed greeting once and propagating `greet`'s `ValueError("name must not be blank")` for invalid input. Existing helpers, CLI behavior and greeting formatting remain unchanged.

## Verification
Pytest and pytest-bdd independently cover `True`, `False`, and invalid input. The registered nmg-sdlc smoke provider must prove issue #131 closed by an exact-head merged PR from its own invocation; static status or an edited success marker is insufficient.
