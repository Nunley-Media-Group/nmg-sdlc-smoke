# Requirements: Add greeting_ascii85 library helper

**Issue**: #290
**Date**: 2026-11-07
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/287-add-greeting-base85-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_ascii85(name)` helper that returns the Ascii85 encoding of the completed greeting
**So that** I can get an Ascii85 text encoding of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The encoding covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is a `str` produced by Python's standard-library `base64.a85encode(...)` with its default arguments, decoded as ASCII: no `<~ ~>` delimiters, no `y` folding of spaces, and no line wrapping. No Unicode normalization is applied.

`greeting_base32`, `greeting_base64`, and `greeting_base85` already return standard-library text encodings of the greeting. `greeting_base85` uses the RFC 1924 alphabet (`base64.b85encode`), which differs from Ascii85. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns an Ascii85 encoding.

## Acceptance Criteria

### AC1: Return the Ascii85 encoding of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_ascii85` with each name
**Then** it returns the `str` `87cURD_*"sA75` for `Ada` and `87cURD_*"sA76TSDg#].@:Nj` for `Ada Lovelace`

### AC2: Encode the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_ascii85` with it
**Then** it returns `87cURD_*#7Do8U`, which equals `base64.a85encode("Hello, Zoë".encode("utf-8")).decode("ascii")`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_ascii85` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_ascii85` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_ascii85("Ada")` returns `87cURD_*"sA75`
**And** `"greeting_ascii85"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the Ascii85 encoding from `base64.a85encode` with default arguments (no `<~ ~>` delimiters, no `y` folding, no line wrapping) of the UTF-8 encoded greeting
- that the encoding covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_ascii85(name: str) -> str` returning `base64.a85encode(greet(name).encode("utf-8")).decode("ascii")` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_ascii85` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the Ascii85 encoding
- Adobe `<~ ~>` framed output, `y` space folding, line wrapping, or Z85
- Decoding Ascii85 back to a greeting
- Unicode normalization of names
- Changes to `greeting_base85` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #290 | 2026-11-07 | Initial feature spec |
