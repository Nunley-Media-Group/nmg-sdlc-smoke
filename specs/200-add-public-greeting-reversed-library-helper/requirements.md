# Requirements: Add public greeting_reversed library helper

**Issue**: #200
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python caller of the `nmg_sdlc_smoke` library
**I want** `greeting_reversed(name)` to return the complete greeting reversed
**So that** I can obtain the reversed greeting text without changing `greet` or the `nmg-smoke` CLI

## Background

`greet(name)` returns `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. The package already exports pure helpers derived from the complete greeting, such as `greeting_casefold`, `greeting_length`, and `greeting_word_count`. Each is re-exported from `nmg_sdlc_smoke`, listed in `nmg_sdlc_smoke.__all__`, and documented in the README Library section. No helper returns the greeting in reverse order.

## Acceptance Criteria

### AC1: Reverse the complete greeting by code point

**Given** the installed `nmg_sdlc_smoke` package
**When** `greeting_reversed("Ada")` and `greeting_reversed("Zoë")` are called (with `ë` as the single precomposed code point U+00EB)
**Then** they return exactly `"adA ,olleH"` and `"ëoZ ,olleH"` respectively

### AC2: Reject invalid names with the existing validation

**Given** the names `""`, `"   "`, and the non-string value `None`
**When** `greeting_reversed` is called with each
**Then** each call raises `ValueError` with message `name must not be blank` and returns no value

### AC3: Export the helper without changing existing surfaces

**Given** the installed package
**When** a caller runs `from nmg_sdlc_smoke import greeting_reversed`, calls `greet("Ada")`, and runs `nmg-smoke Ada`
**Then** the import succeeds and `"greeting_reversed"` is in `nmg_sdlc_smoke.__all__`
**And** `greet("Ada")` returns `"Hello, Ada"` and `nmg-smoke Ada` prints exactly `Hello, Ada` followed by one newline with exit status 0
**And** every name previously listed in `nmg_sdlc_smoke.__all__` remains listed

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add public `greeting_reversed(name: str) -> str` returning `greet(name)` reversed by Unicode code point | Must |
| FR2 | Invalid names propagate `greet`'s `ValueError("name must not be blank")` unchanged | Must |
| FR3 | Export `greeting_reversed` from `nmg_sdlc_smoke` and list it in `__all__`, keeping all existing exports | Must |
| FR4 | Cover AC1–AC3 with pytest unit tests and pytest-bdd scenarios under `tests/features/` | Must |
| FR5 | Document `greeting_reversed` in the README `## Library` import list and examples, including `greeting_reversed("Ada")  # "adA ,olleH"` | Must |

## Out of Scope

- Any `nmg-smoke` CLI flag or output change (including a `--reverse` flag)
- Grapheme-cluster-aware reversal (combining marks and multi-code-point emoji are reversed per code point)
- Changes to `greet`, its validation message, or any other existing helper
- Runtime dependencies

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #200 | 2026-10-06 | Initial feature spec |
