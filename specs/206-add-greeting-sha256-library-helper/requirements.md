# Requirements: Add greeting_sha256 library helper

**Issue**: #206
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_sha256(name)` helper that returns the SHA-256 hex digest of the completed greeting
**So that** I can get a stable fingerprint of the greeting text without re-implementing its encoding and hashing

## Background

`greet(name)` returns `Hello, {name}` for valid names. For empty, whitespace-only, and non-string names it raises `ValueError("name must not be blank")`. Sibling helpers such as `greeting_length`, `greeting_bytes`, and `greeting_casefold` each call `greet(name)` and derive a value from the completed greeting; `greeting_bytes` measures the greeting's UTF-8 encoding. Each helper is defined in `src/nmg_sdlc_smoke/greet.py`, re-exported from `nmg_sdlc_smoke` with a self-aliased import, listed in `nmg_sdlc_smoke.__all__`, and documented in the README Library section. No helper or source module computes a hash or digest.

## Acceptance Criteria

### AC1: Return the SHA-256 hex digest of the completed greeting

**Given** the valid name `Ada`
**When** a caller invokes `greeting_sha256("Ada")`
**Then** it returns the Python `str` `7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66`
**And** that value is the SHA-256 digest of the 10 UTF-8 bytes of `Hello, Ada`, written as exactly 64 lowercase hexadecimal characters

### AC2: Hash the exact UTF-8 code points without normalization

**Given** the valid names `Zoë` spelled with the precomposed `ë` (U+00EB, Python `"Zo\u00eb"`) and `Zoe` followed by the combining diaeresis U+0308 (Python `"Zoe\u0308"`)
**When** a caller invokes `greeting_sha256` with each name
**Then** it returns `aadd4ee82814c54de89ac9cd0e8f089a485196e4952ee920db669caccb7c2524` for the precomposed name
**And** it returns `af1a0a3bab8dec9c18ed0501706ead61457c718667ae4bcfd5a7dbd525192064` for the decomposed name

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_sha256` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no digest

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_sha256` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_sha256("Ada")` returns `7da4681c4837bb56185adc6967f0c6847c33148afb0ba4aefac709465da75f66`
**And** `"greeting_sha256"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the 64-character lowercase hexadecimal return format, that the complete greeting is encoded as UTF-8, that no Unicode normalization is applied, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_sha256(name: str) -> str`. It returns the 64-character lowercase hexadecimal SHA-256 digest of `greet(name)` encoded as UTF-8, with no stripping, case conversion, or Unicode normalization. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and add it to `__all__`, keeping every existing export. Document its import, example result, output format, UTF-8 encoding, absence of normalization, and inherited validation in the README Library section. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change, including a digest flag
- Other hash algorithms (MD5, SHA-1, SHA-512, BLAKE2), keyed or salted hashing, and raw `bytes` digests
- Hashing the name alone
- Applying Unicode normalization, case conversion, or whitespace stripping before hashing
- Changing `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #206 | 2026-10-18 | Initial feature spec |
