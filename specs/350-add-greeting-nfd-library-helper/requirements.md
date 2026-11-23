# Requirements: Add greeting_nfd library helper

**Issue**: #350
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/347-add-greeting-nfc-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_nfd(name)` helper that returns the completed greeting in Unicode Normalization Form D
**So that** I can process greetings character-by-character with base letters and combining marks separated, regardless of whether the name used composed or decomposed characters

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_nfd` returns one `str` equal to `unicodedata.normalize("NFD", greet(name))`:

- Precomposed characters are canonically decomposed into a base character followed by combining marks (for example `é`, U+00E9, becomes `e` + U+0301).
- Text with no decomposable characters is returned unchanged.
- Only canonical decomposition is applied: compatibility characters such as the ligature `ﬁ` (U+FB01) are kept, and no case change, whitespace change, or accent stripping is applied.

## Acceptance Criteria

### AC1: Decompose precomposed characters

**Given** the valid names `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` and `"\N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr\N{LATIN SMALL LETTER O WITH DIAERESIS}m"`
**When** a caller invokes `greeting_nfd` with each name
**Then** they return `"Hello, Chloe\N{COMBINING ACUTE ACCENT}"` (13 code points) and `"Hello, A\N{COMBINING RING ABOVE}ngstro\N{COMBINING DIAERESIS}m"` (17 code points) respectively
**And** `type(result) is str` for each result

### AC2: Leave text without decomposable characters unchanged

**Given** the valid names `Ada`, `Ada Lovelace`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_nfd` with each name
**Then** each result equals `greet(name)`

### AC3: Apply canonical, not compatibility, normalization

**Given** the valid names `"\N{LATIN SMALL LIGATURE FI}ona"` and `"Ada  Lovelace"` (two spaces)
**When** a caller invokes `greeting_nfd` with each name
**Then** they return `"Hello, \N{LATIN SMALL LIGATURE FI}ona"` (11 code points) and `"Hello, Ada  Lovelace"` respectively

### AC4: Agree with unicodedata NFD

**Given** the valid names `Ada`, `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `O'Brien-Smith`
**When** a caller invokes `greeting_nfd` with each name
**Then** the result equals `unicodedata.normalize("NFD", greet(name))`
**And** `unicodedata.is_normalized("NFD", result)` is `True`

### AC5: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_nfd` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC6: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_nfd` and follows the README example
**Then** the import succeeds and the README example `len(greeting_nfd("Chlo\u00e9"))` evaluates to `13`
**And** `"greeting_nfd"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the NFD decomposition rule, the kept compatibility characters, and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_nfd(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `unicodedata.normalize("NFD", greet(name))` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_nfd` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_nfd` in the README Library section (import list, usage example, behavior sentence) consistent with `greeting_nfc` | Should |

## Out of Scope

- NFKC or NFKD helpers, or a configurable normalization-form parameter
- Changes to `greet`, `greeting_nfc`, or the other existing helpers
- A new `nmg-smoke` CLI flag or option for normalized output

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #350 | 2026-11-23 | Initial feature spec |
