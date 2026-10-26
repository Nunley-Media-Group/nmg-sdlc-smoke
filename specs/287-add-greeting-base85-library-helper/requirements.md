# Requirements: Add greeting_base85 library helper

**Issue**: #287
**Date**: 2026-10-26
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/263-add-greeting-base32-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_base85(name)` helper that returns the Base85 encoding of the completed greeting
**So that** I can get a compact text encoding of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The encoding covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is a `str` in the RFC 1924 Base85 alphabet (`0`–`9`, `A`–`Z`, `a`–`z`, and `!#$%&()*+-;<=>?@^_`{|}~`). It comes from Python's standard-library `base64.b85encode(...)` decoded as ASCII, with no padding characters, no `<~ ~>` delimiters, and no line breaks. No Unicode normalization is applied.

`greeting_base32` and `greeting_base64` already return standard-library text encodings of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a Base85 encoding.

## Acceptance Criteria

### AC1: Return the Base85 encoding of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_base85` with each name
**Then** it returns the `str` `NM&qnZ!91|WMK` for `Ada` and `NM&qnZ!91|WMLpoZ+2yDVPj<` for `Ada Lovelace`

### AC2: Encode the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_base85` with it
**Then** it returns `NM&qnZ!92MZ^Nq`, which equals `base64.b85encode("Hello, Zoë".encode("utf-8")).decode("ascii")`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_base85` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_base85` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_base85("Ada")` returns `NM&qnZ!91|WMK`
**And** `"greeting_base85"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the RFC 1924 Base85 encoding from `base64.b85encode` (no padding, delimiters, or line breaks) of the UTF-8 encoded greeting
- that the encoding covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_base85(name: str) -> str` returning `base64.b85encode(greet(name).encode("utf-8")).decode("ascii")` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_base85` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the Base85 encoding
- Adobe Ascii85 (`base64.a85encode`), Z85, or `<~ ~>` framed output
- Decoding Base85 back to a greeting
- Unicode normalization of names
- Changes to `greeting_base32`, `greeting_base64`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #287 | 2026-10-26 | Initial feature spec |
