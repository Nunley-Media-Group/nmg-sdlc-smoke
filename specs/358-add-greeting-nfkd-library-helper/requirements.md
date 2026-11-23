# Requirements: Add greeting_nfkd library helper

**Issue**: #358
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/350-add-greeting-nfd-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_nfkd(name)` helper that returns the completed greeting in Unicode Normalization Form KD
**So that** I can compare and search greetings with compatibility characters folded to their plain equivalents and base letters separated from combining marks

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_nfkd` returns one `str` equal to `unicodedata.normalize("NFKD", greet(name))`:

- Compatibility characters are replaced by their compatibility equivalents (for example the ligature `ﬁ`, U+FB01, becomes `fi`; fullwidth `Ａ`, U+FF21, becomes `A`; superscript `²`, U+00B2, becomes `2`).
- Precomposed characters are decomposed into a base character followed by combining marks (for example `é`, U+00E9, becomes `e` + U+0301).
- Text with no decomposable or compatibility characters is returned unchanged.
- No case change, whitespace collapsing, or accent stripping is applied.

## Acceptance Criteria

### AC1: Fold compatibility characters

**Given** the valid names `"\N{LATIN SMALL LIGATURE FI}ona"`, `"\N{FULLWIDTH LATIN CAPITAL LETTER A}da"`, and `"Ada\N{SUPERSCRIPT TWO}"`
**When** a caller invokes `greeting_nfkd` with each name
**Then** they return `"Hello, fiona"` (12 code points), `"Hello, Ada"` (10 code points), and `"Hello, Ada2"` (11 code points) respectively
**And** `type(result) is str` for each result

### AC2: Decompose precomposed characters

**Given** the valid name `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`
**When** a caller invokes `greeting_nfkd` with it
**Then** it returns `"Hello, Chloe\N{COMBINING ACUTE ACCENT}"` (13 code points)

### AC3: Leave already-normalized text unchanged

**Given** the valid names `Ada`, `"Ada  Lovelace"` (two spaces), and `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_nfkd` with each name
**Then** each result equals `greet(name)`

### AC4: Agree with unicodedata NFKD

**Given** the valid names `Ada`, `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `O'Brien-Smith`
**When** a caller invokes `greeting_nfkd` with each name
**Then** the result equals `unicodedata.normalize("NFKD", greet(name))`
**And** `unicodedata.is_normalized("NFKD", result)` is `True`

### AC5: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_nfkd` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC6: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_nfkd` and follows the README example
**Then** the import succeeds and the README example `greeting_nfkd("\ufb01ona")` evaluates to `"Hello, fiona"`
**And** `"greeting_nfkd"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the NFKD compatibility-and-canonical decomposition rule and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_nfkd(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `unicodedata.normalize("NFKD", greet(name))` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_nfkd` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_nfkd` in the README Library section (import list, usage example, behavior sentence) consistent with `greeting_nfd` | Should |

## Out of Scope

- A configurable normalization-form parameter or a combined normalization helper
- Changes to `greet`, `greeting_nfc`, `greeting_nfd`, `greeting_slug`, an NFKC helper, or the other existing helpers
- A new `nmg-smoke` CLI flag or option for normalized output

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #358 | 2026-11-23 | Initial feature spec |
