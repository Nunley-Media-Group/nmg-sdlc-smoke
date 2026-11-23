# Requirements: Add greeting_json library helper

**Issue**: #368
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_json(name)` helper that returns the completed greeting encoded as a JSON string literal
**So that** I can embed the greeting in JSON output without re-implementing the greeting or the escaping rules

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_json` returns `json.dumps(greet(name))` with the standard library defaults (including `ensure_ascii=True`). It encodes the complete greeting (not the name alone), including the `Hello, ` prefix. The result includes the surrounding double quotes, escapes `"`, `\`, and control characters, and escapes every non-ASCII character as `\uXXXX`, so the result is always ASCII. Decoding it with `json.loads` returns exactly `greet(name)`.

## Acceptance Criteria

### AC1: Encode a plain greeting as a JSON string literal

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_json` with each name
**Then** they return `"Hello, Ada"` and `"Hello, Ada Lovelace"` respectively, including the surrounding double quotes
**And** each result is a `str`

### AC2: Escape quotes, backslashes, control characters, and non-ASCII

**Given** the valid names `Ada "Bo"`, `C:\x`, `Ada<TAB>Bo` (containing a literal tab character), and `\N{LATIN CAPITAL LETTER E WITH ACUTE}mile`
**When** a caller invokes `greeting_json` with each name
**Then** they return `"Hello, Ada \"Bo\""`, `"Hello, C:\\x"`, `"Hello, Ada\tBo"`, and `"Hello, \u00c9mile"` respectively
**And** for every name above the result equals `json.dumps(greet(name))`, is ASCII-only, and `json.loads(result)` equals `greet(name)`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_json` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC4: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_json` and follows the README example
**Then** the import succeeds and printing `greeting_json("Ada")` outputs `"Hello, Ada"` (with the quotes)
**And** `"greeting_json"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents that it applies `json.dumps` with default settings to the complete greeting, escapes non-ASCII as `\uXXXX`, and inherits `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_json(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `json.dumps(greet(name))` with default arguments | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_json` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_json` in the README Library section (import list, usage example, behavior sentence) consistent with the other encoding helpers | Should |

## Out of Scope

- A new `nmg-smoke --json` CLI flag or any CLI change
- A JSON encoding of `greet_many` results or any JSON object/array output
- Preserving non-ASCII characters unescaped (`ensure_ascii=False`)
- Changes to `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #368 | 2026-11-23 | Initial feature spec |
