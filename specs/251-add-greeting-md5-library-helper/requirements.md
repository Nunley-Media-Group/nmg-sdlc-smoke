# Requirements: Add greeting_md5 library helper

**Issue**: #251
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/206-add-greeting-sha256-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_md5(name)` helper that returns the MD5 hex digest of the completed greeting
**So that** I can get a deterministic 128-bit fingerprint of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest is computed over the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is a 32-character lowercase hexadecimal `str` from Python's standard-library `hashlib.md5(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256` already hashes the greeting with `hashlib`. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns an MD5 digest.

## Acceptance Criteria

### AC1: Return the MD5 hex digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_md5` with each name
**Then** it returns the `str` `a4f502ca98cce831af61b0fe0a319382` for `Ada` and `bd0b2e5ea5baf6775e93262ce37d5a4a` for `Ada Lovelace`

### AC2: Hash the UTF-8 encoding of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_md5` with it
**Then** it returns `26ed66c6559b1e033c70ef2301fe0beb`, which equals `hashlib.md5("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_md5` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_md5` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_md5("Ada")` returns `a4f502ca98cce831af61b0fe0a319382`
**And** `"greeting_md5"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the 32-character lowercase hex MD5 digest of the UTF-8 encoded greeting
- that the digest covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_md5(name: str) -> str` returning `hashlib.md5(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_md5` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the MD5 digest
- Other hash algorithms (SHA-1, BLAKE2, SHA-512)
- Returning raw digest bytes or uppercase hex
- Unicode normalization of names
- Changes to `greeting_sha256` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #251 | 2026-10-25 | Initial feature spec |
