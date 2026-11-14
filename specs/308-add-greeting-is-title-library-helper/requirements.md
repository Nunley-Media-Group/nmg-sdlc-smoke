# Requirements: Add greeting_is_title library helper

**Issue**: #308
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/305-add-greeting-is-printable-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_is_title(name)` helper that reports whether the completed greeting is in title case
**So that** I can check a greeting's capitalization without re-implementing the greeting or the check

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper applies Python's `str.istitle()` to the complete greeting, including the `Hello, ` prefix. It returns `True` when every cased word starts with an uppercase character followed only by lowercase characters, and `False` otherwise. No case conversion or Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, example results, and a prose contract line

Existing boolean predicates such as `greeting_is_ascii` and `greeting_is_printable` follow this shape. The `nmg-smoke --titlecase` flag transforms CLI output, but no library helper reports whether a greeting is already in title case.

## Acceptance Criteria

### AC1: Report True for title-cased greetings

**Given** the valid names `Ada`, `Zoë` (with precomposed U+00EB), `Ada Lovelace`, and `O'Neil`
**When** a caller invokes `greeting_is_title` with each name
**Then** each call returns the `bool` value `True`
**And** each result equals `greet(name).istitle()`

### AC2: Report False for greetings that are not title-cased

**Given** the valid names `ada`, `ADA`, `Ada lovelace`, and `McAdam`
**When** a caller invokes `greeting_is_title` with each name
**Then** each call returns the `bool` value `False`
**And** each result equals `greet(name).istitle()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_is_title` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_is_title` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_is_title("Ada")` returns `True`
**And** `"greeting_is_title"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the title-case check on the complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_is_title(name: str) -> bool` returning `greet(name).istitle()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_is_title` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, examples, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Checking the name alone instead of the complete greeting
- Converting a greeting to title case (the existing `--titlecase` CLI flag already does this)
- A `nmg-smoke` CLI flag or option that prints the result
- Unicode normalization of names
- Changes to any existing predicate helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #308 | 2026-11-14 | Initial feature spec |
