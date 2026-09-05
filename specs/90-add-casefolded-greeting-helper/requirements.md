# Requirements: Add casefolded greeting helper

**Issue**: #90
**Date**: 2026-09-05
**Status**: Approved
**Author**: NMG

## User Story
As a maintainer exercising nmg-sdlc #366, I want greeting_casefold(name) to return a Unicode-casefolded greeting so callers can obtain a normalized greeting without changing greet or CLI behavior.

## Current State
The Python package exports greet and several pure greeting helpers but no greeting_casefold.

## Acceptance Criteria
### AC1: Casefold greeting
Given a valid name, when greeting_casefold("Straße") is called, then it returns "hello, strasse"; greeting_casefold("Ada") returns "hello, ada".
### AC2: Preserve validation
Given a blank, whitespace-only, or non-string name, when greeting_casefold is called, then it raises the existing greet ValueError without fabricating a greeting.
### AC3: Preserve existing surfaces
Given the installed package, when greet("Ada") or nmg-smoke Ada runs, then the existing Hello, Ada result and CLI newline remain unchanged; all existing public exports remain available.

## Functional Requirements
- Export greeting_casefold(name: str) -> str from nmg_sdlc_smoke.
- Return greet(name).casefold(); preserve zero runtime dependencies.
- Cover AC1-AC3 with deterministic pytest and pytest-bdd scenarios and update README usage.
- Run pytest, pytest tests/features, and ruff check .; preserve VERSION-driven delivery.

## Out of Scope
New CLI flags, altered validation, dependency changes, unrelated helpers, or production services.

## Change History
| Issue | Date | Summary |
|---|---|---|
| #90 | 2026-09-05 | Fresh consumer smoke for nmg-sdlc #366 |
