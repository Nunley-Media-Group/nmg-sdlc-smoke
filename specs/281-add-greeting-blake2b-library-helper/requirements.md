# Requirements: Add greeting_blake2b library helper

**Issue**: #281
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/278-add-greeting-sha3-224-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_blake2b(name)` helper that returns the BLAKE2b hex digest of the completed greeting
**So that** I can get a BLAKE2b fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. It uses BLAKE2b with its default parameters: a 64-byte digest with no key, salt, or personalization. The result is the 128-character lowercase hexadecimal `str` from Python's standard-library `hashlib.blake2b(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256`, `greeting_sha3_224`, and the other digest helpers already return hex digests of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a BLAKE2 digest.

## Acceptance Criteria

### AC1: Return the BLAKE2b digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_blake2b` with each name
**Then** it returns a 128-character lowercase hexadecimal `str`: `dacd0313406557f10115a4268fb435f4452c16872be1455fdf41b27fdcd3d1e6dba61210d8b48f846b7c23c68527c53c13bb10e794168d286a376d63513939d4` for `Ada`, and `ebd70a8d05430c07e7297ed2b628032e0b795e0c0992d231b3c266f8c84f4b2c90c85ef5ef66c4ce46f821abd5cc39e356339406f1a760e13577e051a30b0e28` for `Ada Lovelace`

### AC2: Hash the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_blake2b` with it
**Then** it returns `b49235eea9e9b2d59d50adee4a2c9c3a47b147d9667afa992d01399bbe083c6e82273588ae669168438369b25238627d10cd0b1511bb5a4735af1780afd55264`, which equals `hashlib.blake2b("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_blake2b` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_blake2b` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_blake2b("Ada")` returns `dacd0313406557f10115a4268fb435f4452c16872be1455fdf41b27fdcd3d1e6dba61210d8b48f846b7c23c68527c53c13bb10e794168d286a376d63513939d4`
**And** `"greeting_blake2b"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the default-parameter BLAKE2b digest of the UTF-8 encoded complete greeting, as 128 lowercase hexadecimal characters
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_blake2b(name: str) -> str` returning `hashlib.blake2b(greet(name).encode("utf-8")).hexdigest()` with default parameters | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_blake2b` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the BLAKE2b digest
- BLAKE2s, SHAKE, or other hash families
- Custom digest sizes, or keyed, salted, or personalized BLAKE2b hashing
- Uppercase, binary (`bytes`), or Base64-encoded digest output
- Unicode normalization of names
- Changes to `greeting_sha3_224` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #281 | 2026-10-25 | Initial feature spec |
