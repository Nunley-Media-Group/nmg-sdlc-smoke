# Requirements: Add public greeting_has_backslash helper

**Issue**: #185
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public predicate for a literal ASCII backslash in the completed greeting
**So that** I can query that greeting without duplicating the check.

## Background

`greet(name)` returns `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. The package already exports literal-character predicates over the completed greeting, such as `greeting_has_slash`, `greeting_has_apostrophe`, `greeting_has_backtick`, and `greeting_has_underscore`, each listed in `nmg_sdlc_smoke.__all__` and documented in the README Library section. It has no backslash predicate.

## Acceptance Criteria

### AC1: Detect a literal backslash

**Given** a valid name `Ada\` (the Python string `"Ada\\"`)
**When** a caller invokes `greeting_has_backslash("Ada\\")`
**Then** it returns Python `True` because the completed greeting `Hello, Ada\` contains a literal `\` (U+005C).

### AC2: Report absence of a literal backslash

**Given** valid names `Ada`, `Ada/` (solidus, U+002F), `Ada＼` (fullwidth reverse solidus, U+FF3C), and `Ada∖` (set minus, U+2216)
**When** a caller invokes `greeting_has_backslash` with each name
**Then** it returns Python `False` for all four because none of the completed greetings contains a literal `\` (U+005C).

### AC3: Preserve invalid-name behavior

**Given** invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_has_backslash` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does.

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_has_backslash` from `nmg_sdlc_smoke` and follows the README examples
**Then** `greeting_has_backslash("Ada\\")` returns `True`, `greeting_has_backslash("Ada")` returns `False`, `greeting_has_backslash` appears in `nmg_sdlc_smoke.__all__`, and the README documents the U+005C-only match and the inherited invalid-name error.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_has_backslash(name: str) -> bool`, which returns whether the completed `greet(name)` contains a literal `\` (U+005C). | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` (including `__all__`) and document its public import, true/false examples, U+005C-only matching, and inherited validation in the README Library section. | Must |

## Out of Scope

- Changing `greet` output or any `nmg-smoke` CLI option.
- Treating `/` (U+002F), `＼` (U+FF3C), `∖` (U+2216), or `⧵` (U+29F5) as a literal `\`.
- Interpreting escape sequences in the name; the check inspects the characters actually present.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #185 | 2026-09-27 | Initial feature spec |
