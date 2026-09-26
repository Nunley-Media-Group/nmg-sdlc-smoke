# Design: Add public greeting_has_exclamation_or_question helper

**Issue**: #163
**Date**: 2026-09-26
**Status**: Approved
**Author**: NMG

## Overview

Add a pure boolean query alongside the existing punctuation helpers. Inspect the completed `greet(name)` string once for literal `!` or `?`, so input validation remains centralized in `greet` and neither the greeting nor the CLI changes.

## Architecture

In `src/nmg_sdlc_smoke/greet.py`, define `greeting_has_exclamation_or_question(name: str) -> bool` near the punctuation queries. Evaluate `greeting = greet(name)` once, then return `"!" in greeting or "?" in greeting`. Do not call two other punctuation helpers, which would construct and validate the greeting twice; `greeting_ends_with_exclamation` produces a new string rather than checking the original. Add a self-aliased package import and an `__all__` entry in `src/nmg_sdlc_smoke/__init__.py` alongside neighboring query exports. In README's Library section add the import, true/false calls, and inherited-validation sentence. The existing package dependencies remain unchanged.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_exclamation_or_question` | `name: str` | `bool`, or `ValueError("name must not be blank")` for invalid input | Return whether the completed `greet(name)` contains literal `!` or `?`; no Unicode lookalikes or added punctuation. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #163 | 2026-09-26 | Initial feature design |
