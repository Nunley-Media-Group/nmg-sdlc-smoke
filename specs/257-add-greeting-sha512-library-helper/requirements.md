# Requirements: Add greeting_sha512 library helper

**Issue**: #257
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/254-add-greeting-sha1-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha512(name)` helper that returns the SHA-512 hex digest of the completed greeting
**So that** I can get a deterministic 512-bit fingerprint of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest is computed over the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is a 128-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha512(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256`, `greeting_md5`, and `greeting_sha1` already hash the greeting with `hashlib`. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA-512 digest.

## Acceptance Criteria

### AC1: Return the SHA-512 hex digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha512` with each name
**Then** it returns the `str` `8abfe44c9cccb8990fcecac86c840fce7ccb1949a4eb49569c0f0cedc1481a8cdac6a37dd286d2d1d8175ebd63ff071b8882052d0a0bd874f88e03ad812215e2` for `Ada` and `6c200b8221e61ef4fa3e4028a8484253f8abf94b0034d52be2224f37d7039c7b081304d248d8b6424c7455c1dac951ddd61968721ef9969f43fb36ea87abbb53` for `Ada Lovelace`

### AC2: Hash the UTF-8 encoding of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha512` with it
**Then** it returns `f93e61e8fa95d7f3f732ba7cd41ab19b7b2bbee43b20e1f1aca2c7ffeac6d39444bbaec839b5cd2e7e5dbc5adb4c651d3c65fa1fb3765fd5cde55509fe5b2e59`, which equals `hashlib.sha512("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha512` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha512` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha512("Ada")` returns `8abfe44c9cccb8990fcecac86c840fce7ccb1949a4eb49569c0f0cedc1481a8cdac6a37dd286d2d1d8175ebd63ff071b8882052d0a0bd874f88e03ad812215e2`
**And** `"greeting_sha512"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the 128-character lowercase hex SHA-512 digest of the UTF-8 encoded greeting
- that the digest covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha512(name: str) -> str` returning `hashlib.sha512(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha512` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA-512 digest
- Other hash algorithms (SHA-384, SHA-224, BLAKE2, SHA-3)
- Returning raw digest bytes or uppercase hex
- Unicode normalization of names
- Changes to `greeting_sha256`, `greeting_sha1`, `greeting_md5`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #257 | 2026-10-25 | Initial feature spec |
