# Requirements: Add greeting_url_encoded library helper

**Issue**: #217
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_url_encoded(name)` helper that returns the completed greeting percent-encoded
**So that** I can embed the greeting in a URL path segment or query value without encoding it myself

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

Sibling helpers such as `greeting_base64` and `greeting_sha256` each call `greet(name)` and return an encoded form of the completed greeting. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper or source module percent-encodes the greeting.

## Acceptance Criteria

### AC1: Return the percent-encoded greeting

**Given** the valid name `Ada`
**When** a caller invokes `greeting_url_encoded("Ada")`
**Then** it returns the Python `str` `Hello%2C%20Ada`

### AC2: Encode reserved characters and UTF-8 bytes, keep unreserved characters

**Given** the valid names `A/B&C~d_e.f` and `Zoë` (precomposed U+00EB)
**When** a caller invokes `greeting_url_encoded` with each name
**Then** it returns `Hello%2C%20A%2FB%26C~d_e.f` and `Hello%2C%20Zo%C3%AB` respectively
**And** `,`, space, `/`, and `&` are percent-encoded with uppercase hex digits, `ë` is encoded as its UTF-8 bytes `%C3%AB`, and ASCII letters, digits, `-`, `.`, `_`, and `~` are unchanged

### AC3: Decoding restores the greeting

**Given** the valid names `Ada`, `Zoë`, and `A/B&C~d_e.f`
**When** `urllib.parse.unquote` is applied to the result of `greeting_url_encoded(name)`
**Then** the result equals `greet(name)` exactly

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_url_encoded` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC5: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_url_encoded` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_url_encoded("Ada")` returns `Hello%2C%20Ada`
**And** `"greeting_url_encoded"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README Library section states that the complete greeting is percent-encoded as UTF-8, that only `A`–`Z`, `a`–`z`, `0`–`9`, `-`, `.`, `_`, and `~` are left unencoded, and that the helper inherits `greet`'s `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_url_encoded(name: str) -> str` returning `greet(name)` percent-encoded as UTF-8 with uppercase hex digits, leaving only the RFC 3986 unreserved characters (`A`–`Z`, `a`–`z`, `0`–`9`, `-`, `.`, `_`, `~`) unencoded. It uses only the standard library. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and add it to `__all__`, keeping every existing export. In the README Library section, document its import, the `greeting_url_encoded("Ada")` example result, the encoding contract, and the inherited validation. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change, including a `--url-encoded` flag
- A decoding helper or `+`-for-space (form) encoding
- Percent-encoding the name alone
- Changing `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #217 | 2026-10-24 | Initial feature spec |
