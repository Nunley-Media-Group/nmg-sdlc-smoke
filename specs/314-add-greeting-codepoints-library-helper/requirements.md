# Requirements: Add greeting_codepoints library helper

**Issue**: #314
**Date**: 2026-11-15
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/311-add-greeting-swapcase-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_codepoints(name)` helper that returns the Unicode code points of the completed greeting
**So that** I can inspect the greeting's characters numerically without re-implementing the greeting

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper returns a new `list[int]` holding `ord(ch)` for each character of the complete greeting, in order, including the `Hello, ` prefix. A character outside the Basic Multilingual Plane contributes exactly one code point. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, example results, and a prose contract line

`greeting_bytes` returns the UTF-8 byte count and `greeting_length` returns the character count, but no helper returns the greeting's code points.

## Acceptance Criteria

### AC1: Return the greeting's code points for valid names

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_codepoints` with each name
**Then** the calls return the `list[int]` values `[72, 101, 108, 108, 111, 44, 32, 65, 100, 97]` and `[72, 101, 108, 108, 111, 44, 32, 90, 111, 235]` respectively
**And** each result equals `[ord(ch) for ch in greet(name)]`

### AC2: Return one code point per non-BMP character

**Given** the valid name `😀` (U+1F600)
**When** a caller invokes `greeting_codepoints` with that name
**Then** the call returns `[72, 101, 108, 108, 111, 44, 32, 128512]`
**And** the result length equals `greeting_length("😀")`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_codepoints` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_codepoints` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_codepoints("Ada")` returns `[72, 101, 108, 108, 111, 44, 32, 65, 100, 97]`
**And** `"greeting_codepoints"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the code-point list of the complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_codepoints(name: str) -> list[int]` returning a new list `[ord(ch) for ch in greet(name)]` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_codepoints` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Any new or changed `nmg-smoke` CLI option
- Formatted code-point strings (for example `U+0048`) or hexadecimal output
- Code points of the name alone instead of the complete greeting
- Unicode normalization of names

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #314 | 2026-11-15 | Initial feature spec |
