# Requirements: Add greeting_sha384 library helper

**Issue**: #260
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/257-add-greeting-sha512-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha384(name)` helper that returns the SHA-384 hex digest of the completed greeting
**So that** I can get a deterministic 384-bit fingerprint of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest is computed over the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is a 96-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha384(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256`, `greeting_sha512`, `greeting_sha1`, and `greeting_md5` already hash the greeting with `hashlib`. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA-384 digest.

## Acceptance Criteria

### AC1: Return the SHA-384 hex digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha384` with each name
**Then** it returns the `str` `81cbed2fa5e07b7ec1d2a13da4de9584c07ddbbb2748dc5711aaafb067c07b03c120099ddcd53135b382c0e3c6198f5d` for `Ada` and `c2dde392dc096399214577c5f80007a7d8a19067f1519f01f84d9c196c17af898991685a268fefc92d7830b3572795db` for `Ada Lovelace`

### AC2: Hash the UTF-8 encoding of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha384` with it
**Then** it returns `b40fde84416eb63cd597533882ee9cd075caa751a9adb0aca24f7a23b6c642d140574c9dde5bb9aa7ac4e9a91209051d`, which equals `hashlib.sha384("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha384` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha384` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha384("Ada")` returns `81cbed2fa5e07b7ec1d2a13da4de9584c07ddbbb2748dc5711aaafb067c07b03c120099ddcd53135b382c0e3c6198f5d`
**And** `"greeting_sha384"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the 96-character lowercase hex SHA-384 digest of the UTF-8 encoded greeting
- that the digest covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha384(name: str) -> str` returning `hashlib.sha384(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha384` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA-384 digest
- Other hash algorithms (SHA-224, BLAKE2, SHA-3)
- Returning raw digest bytes or uppercase hex
- Unicode normalization of names
- Changes to `greeting_sha256`, `greeting_sha512`, `greeting_sha1`, `greeting_md5`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #260 | 2026-10-25 | Initial feature spec |
