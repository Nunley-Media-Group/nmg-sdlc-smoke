# Requirements: Add greeting_blake2s library helper

**Issue**: #284
**Date**: 2026-10-26
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/281-add-greeting-blake2b-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_blake2s(name)` helper that returns the BLAKE2s hex digest of the completed greeting
**So that** I can get a compact BLAKE2s fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The digest covers the complete greeting, including the `Hello, ` prefix, after encoding it as UTF-8. It uses BLAKE2s with its default parameters: a 32-byte digest with no key, salt, or personalization. The result is the 64-character lowercase hexadecimal `str` from Python's standard-library `hashlib.blake2s(...).hexdigest()`. No Unicode normalization is applied.

`greeting_sha256`, `greeting_blake2b`, and the other digest helpers already return hex digests of the greeting. Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

No existing helper returns a BLAKE2s digest.

## Acceptance Criteria

### AC1: Return the BLAKE2s digest of the completed greeting

**Given** the valid names `Ada` and `Ada Lovelace`
**When** a caller invokes `greeting_blake2s` with each name
**Then** it returns a 64-character lowercase hexadecimal `str`: `68d52139de7dbb117ec790dad9989297d2dc4914ebd9b4d177d0e5da344edb14` for `Ada`, and `22f894a44c4420a35fdf533cbb7b73908b46f9e0733f84cc89e964994a9631e7` for `Ada Lovelace`

### AC2: Hash the UTF-8 bytes of non-ASCII greetings

**Given** the valid name `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_blake2s` with it
**Then** it returns `8092041e5f4bb16247b07aa2d091daf95dae26f1a9ad10f3def9ebfe616b4b3b`, which equals `hashlib.blake2s("Hello, Zoë".encode("utf-8")).hexdigest()`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_blake2s` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_blake2s` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_blake2s("Ada")` returns `68d52139de7dbb117ec790dad9989297d2dc4914ebd9b4d177d0e5da344edb14`
**And** `"greeting_blake2s"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is the default-parameter BLAKE2s digest of the UTF-8 encoded complete greeting, as 64 lowercase hexadecimal characters
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_blake2s(name: str) -> str` returning `hashlib.blake2s(greet(name).encode("utf-8")).hexdigest()` with default parameters | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_blake2s` from `nmg_sdlc_smoke` and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the BLAKE2s digest
- Custom digest sizes, or keyed, salted, or personalized BLAKE2s hashing
- Uppercase, binary (`bytes`), or Base64-encoded digest output
- Unicode normalization of names
- Changes to `greeting_blake2b` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #284 | 2026-10-26 | Initial feature spec |
