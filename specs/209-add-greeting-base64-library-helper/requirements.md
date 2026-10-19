# Requirements: Add greeting_base64 library helper

**Issue**: #209
**Date**: 2026-10-18
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_base64(name)` helper that returns the standard Base64 encoding of the completed greeting
**So that** I can get an ASCII-safe text form of the greeting without re-implementing its UTF-8 encoding and Base64 conversion

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

Sibling helpers such as `greeting_bytes`, `greeting_reversed`, and `greeting_sha256` each call `greet(name)` and derive a value from the completed greeting. `greeting_bytes` measures the greeting's UTF-8 encoding, and `greeting_sha256` returns a text digest of those bytes.

Each helper is:
- defined in `src/nmg_sdlc_smoke/greet.py`;
- re-exported from `nmg_sdlc_smoke` with a self-aliased import;
- listed in `nmg_sdlc_smoke.__all__`;
- documented in the README Library section with an import, an example result, and a prose contract line.

No helper or source module performs Base64 encoding.

## Acceptance Criteria

### AC1: Return the Base64 text of the completed greeting

**Given** the valid name `Ada`
**When** a caller invokes `greeting_base64("Ada")`
**Then** it returns the Python `str` `SGVsbG8sIEFkYQ==`
**And** decoding that value with the standard Base64 alphabet yields exactly the 10 UTF-8 bytes of `Hello, Ada`

### AC2: Use the standard alphabet with `=` padding

**Given** the valid names `a?>`, `a>>`, `Bo`, and `Bob~`
**When** a caller invokes `greeting_base64` with each name
**Then** it returns `SGVsbG8sIGE/Pg==` for `a?>` (standard `/`, not URL-safe `_`)
**And** it returns `SGVsbG8sIGE+Pg==` for `a>>` (standard `+`, not URL-safe `-`)
**And** it returns `SGVsbG8sIEJv` for `Bo` (9-byte greeting, no padding)
**And** it returns `SGVsbG8sIEJvYn4=` for `Bob~` (11-byte greeting, one `=`)

### AC3: Encode exact UTF-8 code points without line breaks

**Given** three valid names:
- `Zoë` spelled with the precomposed `ë` (U+00EB, Python `"Zo\u00eb"`)
- `Zoe` followed by the combining diaeresis U+0308 (Python `"Zoe\u0308"`)
- `A` repeated 60 times (Python `"A" * 60`, a 67-byte greeting)

**When** a caller invokes `greeting_base64` with each name
**Then** it returns `SGVsbG8sIFpvw6s=` for the precomposed name
**And** it returns `SGVsbG8sIFpvZcyI` for the decomposed name
**And** for the 60-character name it returns this single 92-character string, which contains no line break characters: `SGVsbG8sIEFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQUFBQQ==`

### AC4: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_base64` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC5: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_base64` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_base64("Ada")` returns `SGVsbG8sIEFkYQ==`
**And** `"greeting_base64"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents four things:
- that the complete greeting (not the name alone) is encoded as UTF-8
- the standard Base64 alphabet (`+`, `/`) with `=` padding and no line breaks
- that the result is a `str` and no Unicode normalization is applied
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Provide `greeting_base64(name: str) -> str`. It returns the RFC 4648 standard-alphabet Base64 encoding of `greet(name)` encoded as UTF-8, with `=` padding and no line breaks, as an ASCII `str`. It applies no stripping, case conversion, or Unicode normalization and uses only the standard library. | Must |
| FR2 | Preserve `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names. | Must |
| FR3 | Export the helper from `nmg_sdlc_smoke` and add it to `__all__`, keeping every existing export. In the README Library section, document its import, an example result, the UTF-8 encoding of the complete greeting, the standard alphabet with padding and no line breaks, the `str` return type without normalization, and the inherited validation. | Must |

## Out of Scope

- Any `nmg-smoke` CLI option or output change, including a `--base64` flag
- URL-safe alphabet, unpadded output, and line-wrapped (MIME) output
- Returning `bytes`
- A Base64 decoding helper
- Encoding the name alone
- Applying Unicode normalization, case conversion, or whitespace stripping before encoding
- Changing `greet` or any existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #209 | 2026-10-18 | Initial feature spec |
