# Requirements: Add greeting_shake_256 library helper

**Issue**: #299
**Date**: 2026-11-13
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/296-add-greeting-shake-128-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_shake_256(name)` helper that returns a fixed-length SHAKE-256 hex digest of the completed greeting
**So that** I can get a deterministic SHAKE-256 fingerprint of a greeting without re-implementing the greeting or its hashing

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

SHAKE-256 is an extendable-output function, so the helper fixes the output length: it always returns 64 bytes of output as a 128-character lowercase hexadecimal `str`, computed as `hashlib.shake_256(greet(name).encode("utf-8")).hexdigest(64)`. The digest covers the complete greeting, including the `Hello, ` prefix. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

`greeting_shake_128` returns a 32-byte SHAKE-128 digest. No existing helper returns a SHAKE-256 digest.

## Acceptance Criteria

### AC1: Return the 64-byte SHAKE-256 hex digest of the greeting

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_shake_256` with each name
**Then** it returns the `str` `51412b094871bbe3e276da7fa1fad8bd4bfae7cfbeb88db9e732d1f32461e67c41e270771c528e629790ba47af4772e92632de0b5b8f63cf801ef7eb8d6a29a7` for `Ada` and `f1548a17e00c5729deeb887a4c5906e0dcdd3ef62f2e0b3a27a34dd94ef06c9a439d43b9dc7f31c5a71c17ea7ee5a946a4e32d2ed0981916c59d5d8a10ece632` for `Zoë`
**And** each result is 128 lowercase hexadecimal characters equal to `hashlib.shake_256(greet(name).encode("utf-8")).hexdigest(64)`

### AC2: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_shake_256` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC3: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_shake_256` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_shake_256("Ada")` returns `51412b094871bbe3e276da7fa1fad8bd4bfae7cfbeb88db9e732d1f32461e67c41e270771c528e629790ba47af4772e92632de0b5b8f63cf801ef7eb8d6a29a7`
**And** `"greeting_shake_256"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents the fixed 64-byte (128 lowercase hexadecimal character) SHAKE-256 output over the UTF-8 encoded complete greeting and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_shake_256(name: str) -> str` returning `hashlib.shake_256(greet(name).encode("utf-8")).hexdigest(64)` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_shake_256` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers (including `greeting_shake_128`), and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A caller-selectable digest length parameter
- A `nmg-smoke` CLI flag or option that prints the digest
- Unicode normalization of names
- Changes to `greeting_shake_128` or any other existing digest or encoding helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #299 | 2026-11-13 | Initial feature spec |
