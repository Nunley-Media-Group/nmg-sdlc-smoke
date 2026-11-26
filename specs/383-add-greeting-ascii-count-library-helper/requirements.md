# Requirements: Add greeting_ascii_count library helper

**Issue**: #383
**Date**: 2026-11-25
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_ascii_count(name)` helper that returns how many ASCII characters the completed greeting contains
**So that** I can measure ASCII content in a greeting without re-implementing the greeting

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`. The library offers `greeting_is_ascii(name)` (a boolean) and `greeting_non_ascii_count(name)` (code points above U+007F), but nothing reports how many characters are ASCII.

`greeting_ascii_count` counts the Unicode code points whose `ord` value is at most 127 in the complete greeting (not the name alone). It counts code points, not UTF-8 bytes or grapheme clusters, and applies no Unicode normalization. For every valid name, `greeting_ascii_count(name) + greeting_non_ascii_count(name) == len(greet(name))`.

## Acceptance Criteria

### AC1: Count ASCII characters in a plain greeting

**Given** the valid names `Ada`, `Zoë` (precomposed U+00EB), and `李雷`
**When** a caller invokes `greeting_ascii_count` with each name
**Then** they return `10`, `9`, and `7` respectively
**And** `type(result) is int` for each result

### AC2: Count code points without normalization

**Given** the valid names `"Zoe\u0308"` (decomposed `e` + U+0308 COMBINING DIAERESIS) and `"Ada \U0001F600"` (U+1F600 GRINNING FACE)
**When** a caller invokes `greeting_ascii_count` with each name
**Then** they return `10` and `11` respectively
**And** for every valid name in AC1 and AC2 the result equals `sum(ord(ch) <= 127 for ch in greet(name))`
**And** for every valid name in AC1 and AC2, `greeting_ascii_count(name) + greeting_non_ascii_count(name) == len(greet(name))`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_ascii_count` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_ascii_count` and follows the README example
**Then** the import succeeds and the README example `greeting_ascii_count("Zo\u00eb")` gives `9`
**And** `"greeting_ascii_count"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README says that it counts code points at or below U+007F in the complete greeting without normalization and inherits `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_ascii_count(name: str) -> int` to `src/nmg_sdlc_smoke/greet.py`, returning the number of code points in `greet(name)` with `ord <= 127` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_ascii_count` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_ascii_count` in the README Library section (import list, usage example, behavior sentence), following the other count helpers | Should |

## Out of Scope

- A CLI flag for `nmg-smoke` exposing the count
- Counting by UTF-8 bytes, grapheme clusters, or after Unicode normalization
- Any change to `greet`, `greeting_is_ascii`, `greeting_non_ascii_count`, or other existing helpers

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #383 | 2026-11-25 | Initial feature spec |
