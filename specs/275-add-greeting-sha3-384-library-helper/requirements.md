# Requirements: Add greeting_sha3_384 library helper

**Issue**: #275
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/272-add-greeting-sha3-512-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha3_384(name)` helper that returns the SHA3-384 hex digest of the completed greeting
**So that** I can get a 384-bit SHA-3 fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is the 96-character lowercase hexadecimal `str` from Python's standard-library `hashlib.sha3_384(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha3_256` and `greeting_sha3_512` already return SHA3-256 and SHA3-512 hex digests of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a SHA3-384 digest.

## Acceptance Criteria

### AC1: Return the SHA3-384 digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_sha3_384` with each name
**Then** it returns a 96-character lowercase hexadecimal `str`: `1a0e27fabec84a7b6ff60b8feb3cb3a8f6c3838c4242005c74f61de0149c524ac44e5f4d417d35726285bd9ee10b470b` for `Ada`, and `251c47136f46312b1918981ecc29cb66876fb6a8023afeb6bd76cee86d3fb37ec6038e70ea082e727343a1e97fb020ea` for `Ada Lovelace`

### AC2: Hash the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_sha3_384` with it
**Then** it returns `191915c174eb9ed3dc8f2f91aeebb7c9da27d307f70004046dbd659dbb482cd4c413750218633f933f2224976b4f2311`, which equals `hashlib.sha3_384("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha3_384` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha3_384` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha3_384("Ada")` returns `1a0e27fabec84a7b6ff60b8feb3cb3a8f6c3838c4242005c74f61de0149c524ac44e5f4d417d35726285bd9ee10b470b`
**And** `"greeting_sha3_384"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the SHA3-384 digest of the UTF-8 encoded complete greeting, as 96 lowercase hexadecimal characters
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_sha3_384(name: str) -> str` returning `hashlib.sha3_384(greet(name).encode("utf-8")).hexdigest()` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_sha3_384` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the SHA3-384 digest
- SHA3-224, SHAKE, or BLAKE2 helpers
- Uppercase, binary (`bytes`), or Base64-encoded digest output
- Unicode normalization of names
- Changes to `greeting_sha3_256`, `greeting_sha3_512`, or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #275 | 2026-10-25 | Initial feature spec |
