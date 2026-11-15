# Requirements: Add greeting_swapcase library helper

**Issue**: #311
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/308-add-greeting-is-title-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_swapcase(name)` helper that returns the completed greeting with its letter case inverted
**So that** I can get a swap-cased greeting without re-implementing the greeting or the case transform

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper applies Python's `str.swapcase()` to the complete greeting, including the `Hello, ` prefix. Uppercase characters become lowercase, lowercase characters become uppercase, and uncased characters (punctuation, spaces, digits) are unchanged. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, example results, and a prose contract line

Existing string transforms such as `greeting_casefold` and `greeting_reversed` follow this shape. The `nmg-smoke --swapcase` flag swap-cases CLI output, but no library helper returns a swap-cased greeting.

## Acceptance Criteria

### AC1: Return the swap-cased greeting for valid names

**Given** the valid names `Ada`, `Zoë` (with precomposed U+00EB), and `O'Neil 42`
**When** a caller invokes `greeting_swapcase` with each name
**Then** the calls return the `str` values `hELLO, aDA`, `hELLO, zOË`, and `hELLO, o'nEIL 42` respectively
**And** each result equals `greet(name).swapcase()`

### AC2: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_swapcase` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC3: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_swapcase` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_swapcase("Ada")` returns `hELLO, aDA`
**And** `"greeting_swapcase"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the case swap of the complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_swapcase(name: str) -> str` returning `greet(name).swapcase()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_swapcase` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output (including `--swapcase`) unchanged | Must |

## Out of Scope

- Changes to the `nmg-smoke --swapcase` CLI flag or any other CLI option
- Other case-transform library helpers (uppercase, lowercase, titlecase)
- Swapping the case of the name alone instead of the complete greeting
- Unicode normalization of names

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #311 | 2026-11-14 | Initial feature spec |
