# Requirements: Add greeting_has_digit library helper

**Issue**: #115
**Date**: 2026-09-22
**Status**: Approved
**Author**: NMG

## User Story
As a maintainer exercising nmg-sdlc #407, I want a pure greeting_has_digit helper to detect decimal digits in completed greetings without changing the existing API or CLI.

## Acceptance Criteria
### AC1: Decimal digit detection
Given a name containing a Unicode decimal digit, when greeting_has_digit("Ada7") or greeting_has_digit("Ada٣") is called, then it returns True; greeting_has_digit("Ada") returns False.
### AC2: Existing input validation
Given blank, whitespace-only, and non-string names, when greeting_has_digit is called, then it raises greet's existing ValueError.
### AC3: Existing surfaces remain stable
Given the installed package and CLI, when greet and nmg-smoke process Ada, then their output remains Hello, Ada and existing public exports stay available.

## Functional Requirements
- Export greeting_has_digit(name: str) -> bool from src/nmg_sdlc_smoke/__init__.py; use greet(name) and Python str.isdecimal for each character.
- Add deterministic pytest and pytest-bdd scenarios for AC1-AC3; document library usage in README.md.
- Run python -m pytest, python -m pytest tests/features, and python -m ruff check .

## Out of Scope
New CLI flags, dependencies, or unrelated helpers.
