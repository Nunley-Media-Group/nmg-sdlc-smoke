# Requirements: Add greeting_sha1 library helper

**Issue**: #254
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/251-add-greeting-md5-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha1(name)` helper that returns the SHA-1 hex digest of the completed greeting
**So that** I can get a deterministic 160-bit fingerprint of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest is computed over the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is a 40-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha1(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256` and `greeting_md5` already hash the greeting with `hashlib`. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA-1 digest.

## Acceptance Criteria

### AC1: Return the SHA-1 hex digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha1` with each name
**Then** it returns the `str` `991f190147e71279d8656214e556b36a22bf73e4` for `Ada` and `8dde18c21e3195df968018b6213efc61d033ec4f` for `Ada Lovelace`

### AC2: Hash the UTF-8 encoding of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha1` with it
**Then** it returns `5e2bef193596dd46528fb36c4ef8625f71c84577`, which equals `hashlib.sha1("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha1` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha1` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha1("Ada")` returns `991f190147e71279d8656214e556b36a22bf73e4`
**And** `"greeting_sha1"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the 40-character lowercase hex SHA-1 digest of the UTF-8 encoded greeting
- that the digest covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha1(name: str) -> str` returning `hashlib.sha1(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha1` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA-1 digest
- Other hash algorithms (SHA-512, BLAKE2, SHA-3)
- Returning raw digest bytes or uppercase hex
- Unicode normalization of names
- Changes to `greeting_sha256`, `greeting_md5`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #254 | 2026-10-25 | Initial feature spec |
