# Requirements: Add greeting_sha3_224 library helper

**Issue**: #278
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/275-add-greeting-sha3-384-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha3_224(name)` helper that returns the SHA3-224 hex digest of the completed greeting
**So that** I can get a 224-bit SHA-3 fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is the 56-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha3_224(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha3_256`, `greeting_sha3_384`, and `greeting_sha3_512` already return SHA-3 hex digests of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA3-224 digest.

## Acceptance Criteria

### AC1: Return the SHA3-224 digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha3_224` with each name
**Then** it returns a 56-character lowercase hexadecimal `str`: `4f8b1b1e2d62e0fc1292bbc88641b8883bcccc2d0087052131c359aa` for `Ada`, and `196e97d0ffcb84a93f4be2879561b59bdf6970263657fb1c057c8886` for `Ada Lovelace`

### AC2: Hash the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha3_224` with it
**Then** it returns `04b9e41ed63e300fa54d7a8fa8f1bf97ef6e2ce4a7c9e61ba6565ed3`, which equals `hashlib.sha3_224("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha3_224` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha3_224` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha3_224("Ada")` returns `4f8b1b1e2d62e0fc1292bbc88641b8883bcccc2d0087052131c359aa`
**And** `"greeting_sha3_224"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the SHA3-224 digest of the UTF-8 encoded complete greeting, as 56 lowercase hexadecimal characters
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha3_224(name: str) -> str` returning `hashlib.sha3_224(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha3_224` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA3-224 digest
- SHAKE or BLAKE2 helpers
- Uppercase, binary (`bytes`), or Base64-encoded digest output
- Unicode normalization of names
- Changes to `greeting_sha224`, `greeting_sha3_256`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #278 | 2026-10-25 | Initial feature spec |
