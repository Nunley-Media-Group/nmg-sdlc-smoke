# Requirements: Add greeting_quoted_printable library helper

**Issue**: #302
**Date**: 2026-11-13
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/293-add-greeting-html-escaped-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_quoted_printable(name)` helper that returns the quoted-printable encoding of the completed greeting
**So that** I can get a 7-bit-safe, mostly human-readable form of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper encodes the UTF-8 bytes of the complete greeting, including the `Hello, ` prefix, with `quopri.encodestring` and its defaults (`quotetabs=False`, `header=False`), and returns the result decoded as ASCII to a `str`. Printable ASCII other than `=` passes through unchanged, `=` and non-ASCII bytes become `=XX` escapes with uppercase hex digits, and trailing whitespace is escaped. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

Existing encoding helpers (`greeting_base32`, `greeting_base64`, `greeting_base85`, `greeting_ascii85`, `greeting_rot13`, `greeting_url_encoded`, `greeting_html_escaped`) follow this shape. No existing helper returns a quoted-printable encoding.

## Acceptance Criteria

### AC1: Return the quoted-printable encoding of the greeting

**Given** the valid names `Ada`, `Zoë` (with precomposed U+00EB), `a=b`, and `Ada ` (one trailing space)
**When** a caller invokes `greeting_quoted_printable` with each name
**Then** it returns the `str` values `Hello, Ada`, `Hello, Zo=C3=AB`, `Hello, a=3Db`, and `Hello, Ada=20` respectively
**And** each result equals `quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")`

### AC2: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_quoted_printable` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC3: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_quoted_printable` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_quoted_printable("Zoë")` returns `Hello, Zo=C3=AB`
**And** `"greeting_quoted_printable"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the quoted-printable encoding of the UTF-8 encoded complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_quoted_printable(name: str) -> str` returning `quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_quoted_printable` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A quoted-printable decoding helper
- Caller-selectable `quotetabs` or `header` options
- A `nmg-smoke` CLI flag or option that prints the encoding
- Unicode normalization of names
- Changes to any existing encoding or digest helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #302 | 2026-11-13 | Initial feature spec |
