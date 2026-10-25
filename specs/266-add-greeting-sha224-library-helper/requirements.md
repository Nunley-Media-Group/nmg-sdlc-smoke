# Requirements: Add greeting_sha224 library helper

**Issue**: #266
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/260-add-greeting-sha384-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha224(name)` helper that returns the SHA-224 hex digest of the completed greeting
**So that** I can get a compact SHA-2 fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is the 56-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha224(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256`, `greeting_sha384`, and `greeting_sha512` already return SHA-2 hex digests of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA-224 digest.

## Acceptance Criteria

### AC1: Return the SHA-224 digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha224` with each name
**Then** it returns the 56-character lowercase hexadecimal `str` `316233754fcc3ee5160b0102d33639e694a894f689633ca5d2d679ad` for `Ada` and `6c95a9a2f1662a38e55f0dae7e56c9709d0fdd7d04e3223b20042cdb` for `Ada Lovelace`

### AC2: Hash the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha224` with it
**Then** it returns `b35858e7d09007e76d4b898e16cb61920b4dd2a04b3fc64cdbf0fe68`, which equals `hashlib.sha224("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha224` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha224` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha224("Ada")` returns `316233754fcc3ee5160b0102d33639e694a894f689633ca5d2d679ad`
**And** `"greeting_sha224"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the SHA-224 digest of the UTF-8 encoded complete greeting, as 56 lowercase hexadecimal characters
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha224(name: str) -> str` returning `hashlib.sha224(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha224` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA-224 digest
- Uppercase, binary (`bytes`), or Base64-encoded digest output
- SHA-3, BLAKE2, or other hash families
- Unicode normalization of names
- Changes to `greeting_sha256`, `greeting_sha384`, `greeting_sha512`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #266 | 2026-10-25 | Initial feature spec |
