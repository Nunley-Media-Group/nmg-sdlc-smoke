# Requirements: Add greeting_nfc library helper

**Issue**: #347
**Date**: 2026-11-22
**Status**: Approved
**Author**: NMG

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_nfc(name)` helper that returns the completed greeting in Unicode Normalization Form C
**So that** I can compare, store, or measure greetings consistently regardless of whether the name used composed or decomposed characters

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_nfc` returns one `str` equal to `unicodedata.normalize("NFC", greet(name))`:

- Base characters followed by combining marks are composed where Unicode defines a precomposed character (for example `e` + U+0301 becomes `é`, U+00E9).
- Already-composed text is returned unchanged.
- Only canonical composition is applied: compatibility characters such as the ligature `ﬁ` (U+FB01) are kept, and no case change, whitespace change, or accent stripping is applied.

## Acceptance Criteria

### AC1: Compose decomposed characters

**Given** the valid names `"Chloe\N{COMBINING ACUTE ACCENT}"` and `"A\N{COMBINING RING ABOVE}ngstro\N{COMBINING DIAERESIS}m"`
**When** a caller invokes `greeting_nfc` with each name
**Then** they return `"Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` (12 code points) and `"Hello, \N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr\N{LATIN SMALL LETTER O WITH DIAERESIS}m"` (15 code points) respectively
**And** `type(result) is str` for each result

### AC2: Leave already-composed text unchanged

**Given** the valid names `Ada`, `Ada Lovelace`, and `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`
**When** a caller invokes `greeting_nfc` with each name
**Then** each result equals `greet(name)`

### AC3: Apply canonical, not compatibility, normalization

**Given** the valid names `"\N{LATIN SMALL LIGATURE FI}ona"` and `"Ada  Lovelace"` (two spaces)
**When** a caller invokes `greeting_nfc` with each name
**Then** they return `"Hello, \N{LATIN SMALL LIGATURE FI}ona"` (11 code points) and `"Hello, Ada  Lovelace"` respectively

### AC4: Agree with unicodedata NFC

**Given** the valid names `Ada`, `"Chloe\N{COMBINING ACUTE ACCENT}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `O'Brien-Smith`
**When** a caller invokes `greeting_nfc` with each name
**Then** the result equals `unicodedata.normalize("NFC", greet(name))`
**And** `unicodedata.is_normalized("NFC", result)` is `True`

### AC5: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_nfc` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC6: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_nfc` and follows the README example
**Then** the import succeeds and the README example `greeting_nfc("Chloe\u0301")` prints `Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}`
**And** `"greeting_nfc"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the NFC composition rule, the kept compatibility characters, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_nfc(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `unicodedata.normalize("NFC", greet(name))` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_nfc` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_nfc` in the README Library section (import list, usage example, behavior sentence) consistent with the other string-transform helpers | Should |

## Out of Scope

- NFD, NFKC, or NFKD helpers, or a configurable normalization-form parameter
- Changes to `greet`, `greeting_slug`, or the other existing helpers
- A new `nmg-smoke` CLI flag or option for normalized output

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #347 | 2026-11-22 | Initial feature spec |
