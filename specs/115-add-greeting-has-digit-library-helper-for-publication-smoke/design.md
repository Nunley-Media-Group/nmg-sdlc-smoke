# Design: Add greeting_has_digit helper

**Issue**: #115
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## Approach
Add a typed pure function to src/nmg_sdlc_smoke/greet.py returning any(character.isdecimal() for character in greet(name)). Export it through src/nmg_sdlc_smoke/__init__.py. Reusing greet preserves the existing ValueError. No CLI or dependency changes.

## Verification
Cover ASCII and Unicode decimal digits, digit-free greetings, invalid names, and unchanged greet/CLI behavior through pytest and pytest-bdd. Run the manifest-registered Python checks and preserve the VERSION-driven delivery contract.
