# Requirements: Add greeting_hex library helper

**Issue**: #212
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/209-add-greeting-base64-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_hex(name)` helper that returns the lowercase hexadecimal encoding of the completed greeting's UTF-8 bytes
**So that** I can get a byte-exact, ASCII-only text form of the greeting without re-implementing its UTF-8 encoding and hex conversion

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

Sibling helpers such as `greeting_bytes`, `greeting_sha256`, and `greeting_base64` each call `greet(name)` and derive a value from the completed greeting's UTF-8 bytes. Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper returns the hexadecimal encoding of the greeting's bytes.

## Acceptance Criteria

### AC1: Return the hex text of the completed greeting

**Given** the valid name `Ada`
**When** a caller invokes `greeting_hex("Ada")`
**Then** it returns the Python `str` `48656c6c6f2c20416461`
**And** the result is 20 characters long, two per UTF-8 byte of `Hello, Ada`

### AC2: Encode exact UTF-8 code points as lowercase hex without separators

**Given** three valid names:
- `Zoë` with the precomposed `ë` (U+00EB, Python `"Zoë"`)
- `Zoe` followed by the combining diaeresis U+0308 (Python `"Zoë"`)
- `é中` (U+00E9 followed by U+4E2D, Python `"é中"`)

**When** a caller invokes `greeting_hex` with each name
**Then** it returns `48656c6c6f2c205a6fc3ab` for the precomposed name
**And** it returns `48656c6c6f2c205a6f65cc88` for the decomposed name
**And** it returns `48656c6c6f2c20c3a9e4b8ad` for `é中`
**And** every result contains only the characters `0`–`9` and `a`–`f`, with no spaces, colons, or other separators

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_hex` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_hex` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_hex("Ada")` returns `48656c6c6f2c20416461`
**And** `"greeting_hex"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents four things:
- that the complete greeting (not the name alone) is encoded as UTF-8
- that the result is a lowercase hex `str` with two characters per byte and no separators or prefix
- that no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_hex(name: str) -> str`. It returns the lowercase hexadecimal encoding of `greet(name)` encoded as UTF-8, two characters per byte, with no separators or prefix. It applies no stripping, case conversion, or Unicode normalization and uses only the standard library. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and add it to `__all__`, keeping every existing export. In the README Library section, document its import, an example result, the UTF-8 encoding of the complete greeting, the lowercase no-separator format, the absence of normalization, and the inherited validation. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change, including a `--hex` flag
- Uppercase hex, separators, or a `0x` prefix
- Returning `bytes`
- A hex decoding helper
- Encoding the name alone
- Applying Unicode normalization, case conversion, or whitespace stripping before encoding
- Changing `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #212 | 2026-10-24 | Initial feature spec |
