# Requirements: Add greeting_is_printable library helper

**Issue**: #305
**Date**: 2026-11-14
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/57-add-greeting-is-ascii-library-function/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_is_printable(name)` helper that reports whether the completed greeting contains only printable characters
**So that** I can tell whether a greeting is safe to display on one line without re-implementing the greeting or the check

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper checks the complete greeting, including the `Hello, ` prefix, with Python's `str.isprintable()`. It returns `True` when every character is printable and `False` when any character is not, such as a tab or newline. The ASCII space counts as printable. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

Existing boolean predicates such as `greeting_is_ascii` and `greeting_starts_with_hello` follow this shape. No printable-character helper exists.

## Acceptance Criteria

### AC1: Report True for fully printable greetings

**Given** the valid names `Ada`, `Zoë` (with precomposed U+00EB), and `Ada Lovelace`
**When** a caller invokes `greeting_is_printable` with each name
**Then** each call returns the `bool` value `True`
**And** each result equals `greet(name).isprintable()`

### AC2: Report False when the greeting contains a non-printable character

**Given** the valid names `Ada\tLovelace` (with a tab) and `Ada\n` (with a trailing newline)
**When** a caller invokes `greeting_is_printable` with each name
**Then** each call returns the `bool` value `False`
**And** each result equals `greet(name).isprintable()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_is_printable` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_is_printable` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_is_printable("Ada")` returns `True`
**And** `"greeting_is_printable"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the printable check on the complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_is_printable(name: str) -> bool` returning `greet(name).isprintable()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_is_printable` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Checking the name alone instead of the complete greeting
- Stripping or escaping non-printable characters
- A `nmg-smoke` CLI flag or option that prints the result
- Unicode normalization of names
- Changes to any existing predicate helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #305 | 2026-11-14 | Initial feature spec |
