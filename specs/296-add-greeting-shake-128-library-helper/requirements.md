# Requirements: Add greeting_shake_128 library helper

**Issue**: #296
**Date**: 2026-11-09
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/284-add-greeting-blake2s-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_shake_128(name)` helper that returns a fixed-length SHAKE-128 hex digest of the completed greeting
**So that** I can obtain a deterministic extendable-output fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

SHAKE-128 is an extendable-output function, so the helper fixes the output length: it always returns 32 bytes of output as a 64-character lowercase hexadecimal `str`, computed as `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)`. The digest covers the complete greeting, including the `Hello, ` prefix. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

Existing digest helpers (`greeting_md5`, `greeting_sha1`, the SHA-2 and SHA3 families, `greeting_blake2b`, `greeting_blake2s`) return fixed-length hex digests. No existing helper returns a SHAKE digest.

## Acceptance Criteria

### AC1: Return the 32-byte SHAKE-128 hex digest of the greeting

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_shake_128` with each name
**Then** it returns the `str` `a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774` for `Ada` and `8479a68098ec2f7e622cd2c40a917d3a8b79221a308ebde33c5825dc6f0b4b3f` for `Zoë`
**And** each result is 64 lowercase hexadecimal characters equal to `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)`

### AC2: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_shake_128` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC3: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_shake_128` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_shake_128("Ada")` returns `a3930308111b74c13946954b166ee4057689ba55b2b95de0cebdf8f299818774`
**And** `"greeting_shake_128"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the fixed 32-byte (64 lowercase hexadecimal character) SHAKE-128 output over the UTF-8 encoded complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_shake_128(name: str) -> str` returning `hashlib.shake_128(greet(name).encode("utf-8")).hexdigest(32)` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_shake_128` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A caller-selectable digest length parameter
- A `greeting_shake_256` helper
- A `nmg-smoke` CLI flag or option that prints the digest
- Unicode normalization of names
- Changes to any existing digest or encoding helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #296 | 2026-11-09 | Initial feature spec |
