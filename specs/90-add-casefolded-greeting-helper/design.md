# Design: Add casefolded greeting helper

**Issue**: #90
**Date**: 2026-09-05
**Status**: Approved
**Author**: NMG

## Approach
Add a pure typed helper to src/nmg_sdlc_smoke/greet.py returning greet(name).casefold(), and export it through src/nmg_sdlc_smoke/__init__.py without removing existing names. Reuse existing validation through greet. No CLI or dependency changes. Unicode casefold, not lower, is the observable normalization contract.

## Verification
Cover Unicode casefold (Straße), ASCII (Ada), invalid inputs and unchanged existing library/CLI with pytest and pytest-bdd. Run all three registered checks. Preserve current project structure, zero runtime dependencies, and VERSION source.
