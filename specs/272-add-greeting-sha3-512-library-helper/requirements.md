# Requirements: Add greeting_sha3_512 library helper

**Issue**: #272
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/269-add-greeting-sha3-256-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha3_512(name)` helper that returns the SHA3-512 hex digest of the completed greeting
**So that** I can get a 512-bit SHA-3 fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is the 128-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha3_512(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha3_256` already returns a SHA3-256 hex digest of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA3-512 digest.

## Acceptance Criteria

### AC1: Return the SHA3-512 digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha3_512` with each name
**Then** it returns a 128-character lowercase hexadecimal `str`: `0817552f59fade788cc6bfaff1161167b75c5f73a5c0f314be498ad984301ae1a4adf9b9770cd68d4af5d3093d061a5e3b6b306117803a6f359d98cb862a8611` for `Ada`, and `bf622c26b158a44d6a61e0bd31c47969aba0d2e1109acc5156d0f7c451ad696d297677c9d6653d8eedcfd3d9e1ccc8d7efb15e6ab533d5bc44e166c1504556d6` for `Ada Lovelace`

### AC2: Hash the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha3_512` with it
**Then** it returns `ca8d59e8b815479a8cfffe904e4bd8320d68db5529d4e07ad24b507a4feb48ee8babafe94bc865e8c1211281c038a339eb9e5e40a25335bfa01325de6fae177c`, which equals `hashlib.sha3_512("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha3_512` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha3_512` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha3_512("Ada")` returns `0817552f59fade788cc6bfaff1161167b75c5f73a5c0f314be498ad984301ae1a4adf9b9770cd68d4af5d3093d061a5e3b6b306117803a6f359d98cb862a8611`
**And** `"greeting_sha3_512"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the SHA3-512 digest of the UTF-8 encoded complete greeting, as 128 lowercase hexadecimal characters
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha3_512(name: str) -> str` returning `hashlib.sha3_512(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha3_512` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA3-512 digest
- SHA3-224, SHA3-384, SHAKE, or BLAKE2 helpers
- Uppercase, binary (`bytes`), or Base64-encoded digest output
- Unicode normalization of names
- Changes to `greeting_sha3_256` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #272 | 2026-10-25 | Initial feature spec |
