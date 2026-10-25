# Requirements: Add greeting_crc32 library helper

**Issue**: #245
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/206-add-greeting-sha256-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_crc32(name)` helper that returns the CRC-32 checksum of the completed greeting
**So that** I can get a compact, deterministic integer fingerprint of a greeting without re-implementing the greeting or the checksum encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The checksum is computed over the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is the unsigned 32-bit value returned by Python's standard-library `zlib.crc32`, in the range `0` to `4294967295`. No Unicode normalization is applied.

The digest and encoding helpers `greeting_sha256`, `greeting_base64`, `greeting_rot13`, and `greeting_url_encoded` use only the standard library. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`;
- a self-aliased re-export from `nmg_sdlc_smoke`;
- an entry in `nmg_sdlc_smoke.__all__`;
- a README Library entry with an import, an example result, and a prose contract line.

No existing helper returns a CRC-32 checksum.

## Acceptance Criteria

### AC1: Return the CRC-32 checksum of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_crc32` with each name
**Then** it returns the Python `int` `2761732226` for `Ada` and `2495651459` for `Ada Lovelace`

### AC2: Checksum the UTF-8 encoding of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_crc32` with it
**Then** it returns `2271742533`, which equals `zlib.crc32("Hello, Zoë".encode("utf-8"))`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_crc32` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_crc32` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_crc32("Ada")` returns `2761732226`
**And** `"greeting_crc32"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the unsigned CRC-32 `int` of the UTF-8 encoded greeting
- that the checksum covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_crc32(name: str) -> int` returning `zlib.crc32(greet(name).encode("utf-8"))`, an unsigned `int` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_crc32` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, example, and prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Other checksum or hash algorithms (Adler-32, MD5, SHA-1, SHA-512, BLAKE2)
- Seeded or running CRC values, and hex-formatted output
- A `nmg-smoke` CLI flag or option exposing the checksum

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #245 | 2026-10-25 | Initial feature spec |
