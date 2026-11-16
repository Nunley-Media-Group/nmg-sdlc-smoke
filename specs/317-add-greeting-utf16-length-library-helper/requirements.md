# Requirements: Add greeting_utf16_length library helper

**Issue**: #317
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/314-add-greeting-codepoints-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_utf16_length(name)` helper that returns the number of UTF-16 code units in the completed greeting
**So that** I can size the greeting for UTF-16 consumers without re-implementing the greeting

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper returns an `int`: the number of UTF-16 code units in the complete greeting, including the `Hello, ` prefix. The count excludes any byte-order mark. A Basic Multilingual Plane character counts as one unit. A character outside it counts as two units (a surrogate pair). No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, example results, and a prose contract line

`greeting_length` returns the code-point count and `greeting_bytes` returns the UTF-8 byte count. No helper returns the UTF-16 code-unit count.

## Acceptance Criteria

### AC1: Count UTF-16 code units for BMP names

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_utf16_length` with each name
**Then** both calls return the `int` value `10`
**And** each result equals `len(greet(name).encode("utf-16-le")) // 2`

### AC2: Count a surrogate pair for non-BMP characters

**Given** the valid name `😀` (U+1F600)
**When** a caller invokes `greeting_utf16_length` with that name
**Then** the call returns `9`
**And** the result is one greater than `greeting_length("😀")`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_utf16_length` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_utf16_length` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_utf16_length("Ada")` returns `10`
**And** `"greeting_utf16_length"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the UTF-16 code-unit count of the complete greeting, the two-unit count for non-BMP characters, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_utf16_length(name: str) -> int` returning `len(greet(name).encode("utf-16-le")) // 2` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_utf16_length` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- Returning the UTF-16 encoded bytes or code units themselves (only the count)
- UTF-16 counts of the name alone instead of the complete greeting
- Unicode normalization of names

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #317 | 2026-11-15 | Initial feature spec |
