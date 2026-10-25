# Requirements: Add greeting_adler32 library helper

**Issue**: #248
**Date**: 2026-10-25
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/245-add-greeting-crc32-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_adler32(name)` helper that returns the Adler-32 checksum of the completed greeting
**So that** I can get a fast, deterministic integer fingerprint of a greeting without re-implementing the greeting or its encoding

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The checksum is computed over the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. The result is the unsigned 32-bit value returned by Python's standard-library `zlib.adler32`, in the range `0` to `4294967295`. No Unicode normalization is applied.

The checksum helper `greeting_crc32` already uses `zlib` from the standard library. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`;
- a self-aliased re-export from `nmg_sdlc_smoke`;
- an entry in `nmg_sdlc_smoke.__all__`;
- a README Library entry with an import, an example result, and a prose contract line.

No existing helper returns an Adler-32 checksum.

## Acceptance Criteria

### AC1: Return the Adler-32 checksum of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_adler32` with each name
**Then** it returns the Python `int` `312279879` for `Ada` and `1063257746` for `Ada Lovelace`

### AC2: Checksum the UTF-8 encoding of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_adler32` with it
**Then** it returns `400032888`, which equals `zlib.adler32("Hello, Zoë".encode("utf-8"))`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_adler32` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_adler32` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_adler32("Ada")` returns `312279879`
**And** `"greeting_adler32"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the unsigned Adler-32 `int` of the UTF-8 encoded greeting
- that the checksum covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_adler32(name: str) -> int` returning `zlib.adler32(greet(name).encode("utf-8"))`, an unsigned `int` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_adler32` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, example, and prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- Other checksum or hash algorithms (MD5, SHA-1, SHA-512, BLAKE2)
- Seeded or running Adler-32 values, and hex-formatted output
- A `nmg-smoke` CLI flag or option exposing the checksum
- Changes to `greeting_crc32` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #248 | 2026-10-25 | Initial feature spec |
