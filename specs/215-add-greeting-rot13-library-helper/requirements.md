# Requirements: Add greeting_rot13 library helper

**Issue**: #215
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_rot13(name)` helper that returns the completed greeting with ROT13 applied
**So that** I can get a reversible, letter-obscured form of the greeting without re-implementing the rotation

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

Sibling helpers such as `greeting_reversed`, `greeting_casefold`, and `greeting_base64` each call `greet(name)` and return a transformed form of the completed greeting.

Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper or source module applies ROT13 or any letter rotation.

## Acceptance Criteria

### AC1: Return the ROT13 form of the completed greeting

**Given** the valid name `Ada`
**When** a caller invokes `greeting_rot13("Ada")`
**Then** it returns the Python `str` `Uryyb, Nqn`

### AC2: Rotate only ASCII letters and leave every other character unchanged

**Given** the valid names `Mary-Jane O'Neil`, `Zoë` (precomposed U+00EB), and `Ｚed 42` (fullwidth `Ｚ`, U+FF3A)
**When** a caller invokes `greeting_rot13` with each name
**Then** it returns `Uryyb, Znel-Wnar B'Arvy`, `Uryyb, Mbë`, and `Uryyb, Ｚrq 42` respectively
**And** the punctuation, spaces, digits, `ë`, and `Ｚ` are unchanged and letter case is preserved

### AC3: Applying ROT13 twice restores the greeting

**Given** the valid names `Ada`, `Zoë`, and `Mary-Jane O'Neil`
**When** ROT13 is applied to the result of `greeting_rot13(name)` with Python's `codecs.encode(..., "rot13")`
**Then** the result equals `greet(name)` exactly

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_rot13` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC5: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_rot13` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_rot13("Ada")` returns `Uryyb, Nqn`
**And** `"greeting_rot13"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README Library section states that only ASCII letters `A`–`Z` and `a`–`z` are rotated, all other characters are unchanged, and the helper inherits `greet`'s `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_rot13(name: str) -> str` returning `greet(name)` with each ASCII letter rotated 13 places within its case (`A`–`Z`, `a`–`z`) and every other character, including non-ASCII letters, left unchanged. It uses only the standard library. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and add it to `__all__`, keeping every existing export. In the README Library section, document its import, the `greeting_rot13("Ada")` example result, ASCII-only rotation, and the inherited validation. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change, including a `--rot13` flag
- Other rotation amounts (ROT5, ROT47, arbitrary Caesar shifts) or a separate decoding helper
- Rotation of non-ASCII letters
- Rotating the name alone
- Changing `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #215 | 2026-10-24 | Initial feature spec |
