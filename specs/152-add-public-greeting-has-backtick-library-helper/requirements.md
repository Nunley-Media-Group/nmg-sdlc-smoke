# Requirements: Add public greeting_has_backtick library helper

**Issue**: #152
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** Python library caller
**I want** to query whether a completed greeting contains a literal ASCII backtick
**So that** I can inspect the generated text without changing greeting or CLI behavior.

## Background

`greet(name)` produces `Hello, {name}` for valid names and raises `ValueError("name must not be blank")` for blank or non-string names. Existing public punctuation helpers inspect the completed greeting; no backtick helper is available.

## Acceptance Criteria

### AC1: Detect an ASCII backtick

**Given** the public `nmg_sdlc_smoke` library and valid name "Ada`"
**When** ``greeting_has_backtick("Ada`")`` is called
**Then** it returns Python `True` because ``greet("Ada`")`` is "Hello, Ada`" and contains literal ASCII U+0060.

### AC2: Reject absence and a Unicode lookalike

**Given** valid names `Ada` and `Ada｀` (U+FF40 FULLWIDTH GRAVE ACCENT)
**When** `greeting_has_backtick` is called with each name
**Then** both results are Python `False`; the completed greetings are `"Hello, Ada"` and `"Hello, Ada｀"` with no normalization or lookalike matching.

### AC3: Inherit invalid-name behavior

**Given** invalid names `""`, `" \t\n"`, `None`, and `42`
**When** `greeting_has_backtick(name)` is called for each
**Then** every call raises `ValueError("name must not be blank")` as `greet(name)` does.

### AC4: Preserve greeting and CLI output

**Given** the new helper is exported from the public package and the installed `nmg-smoke` console script
**When** a caller evaluates `greet("Ada")` and runs `nmg-smoke Ada`
**Then** `greet("Ada")` is `"Hello, Ada"` and the CLI exits 0 with stdout `"Hello, Ada\n"` and empty stderr.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Export `greeting_has_backtick(name: str) -> bool` from `nmg_sdlc_smoke`; return whether the completed `greet(name)` contains literal ASCII backtick U+0060. | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names. | Must |
| FR3 | Compare literal characters without normalizing or treating Unicode lookalikes such as U+FF40 as backticks. | Must |
| FR4 | Leave `greet`'s result and `nmg-smoke` output unchanged. | Must |
| FR5 | Cover backtick presence, absence, fullwidth lookalike, invalid inputs, and unchanged greeting/CLI with deterministic pytest unit and pytest-bdd scenarios. | Must |

## Out of Scope

- New CLI flags, changed greeting formatting, and detection of other punctuation.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #152 | 2026-09-24 | Initial feature spec |
