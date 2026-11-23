# Requirements: Add greeting_nfkc library helper

**Issue**: #356
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/350-add-greeting-nfd-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_nfkc(name)` helper that returns the completed greeting in Unicode Normalization Form KC
**So that** I can compare and search greetings with compatibility variants (ligatures, full-width letters, no-break spaces) folded to their standard composed equivalents

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

`greeting_nfkc` returns one `str` equal to `unicodedata.normalize("NFKC", greet(name))`:

- Compatibility characters are replaced by their standard equivalents (for example the ligature `ﬁ`, U+FB01, becomes `fi`; full-width `Ａｄａ` becomes `Ada`; a no-break space, U+00A0, becomes a regular space).
- The result is then canonically composed, so a base letter followed by a combining mark becomes the precomposed character (for example `e` + U+0301 becomes `é`).
- Text with no compatibility or composable characters is returned unchanged. No case change, whitespace collapsing, or accent stripping is applied.

## Acceptance Criteria

### AC1: Replace compatibility characters

**Given** the valid names `"\N{LATIN SMALL LIGATURE FI}ona"`, `"\N{FULLWIDTH LATIN CAPITAL LETTER A}\N{FULLWIDTH LATIN SMALL LETTER D}\N{FULLWIDTH LATIN SMALL LETTER A}"`, and `"Ada\N{NO-BREAK SPACE}Lovelace"`
**When** a caller invokes `greeting_nfkc` with each name
**Then** they return `"Hello, fiona"` (12 code points), `"Hello, Ada"` (10 code points), and `"Hello, Ada Lovelace"` (19 code points) respectively
**And** `type(result) is str` for each result

### AC2: Compose decomposed characters

**Given** the valid name `"Chloe\N{COMBINING ACUTE ACCENT}"`
**When** a caller invokes `greeting_nfkc` with it
**Then** it returns `"Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` (12 code points)

### AC3: Leave already-normalized text unchanged

**Given** the valid names `Ada`, `"Ada  Lovelace"` (two spaces), and `O'Brien-Smith`
**When** a caller invokes `greeting_nfkc` with each name
**Then** each result equals `greet(name)`

### AC4: Agree with unicodedata NFKC

**Given** the valid names `Ada`, `"Chloe\N{COMBINING ACUTE ACCENT}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `O'Brien-Smith`
**When** a caller invokes `greeting_nfkc` with each name
**Then** the result equals `unicodedata.normalize("NFKC", greet(name))`
**And** `unicodedata.is_normalized("NFKC", result)` is `True`

### AC5: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_nfkc` with each one
**Then** each call raises `ValueError` with the message `name must not be blank`

### AC6: Expose and document the helper

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller runs `from nmg_sdlc_smoke import greeting_nfkc` and follows the README example
**Then** the import succeeds and the README example `greeting_nfkc("ﬁona")` evaluates to `"Hello, fiona"`
**And** `"greeting_nfkc"` is listed in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** the README documents the NFKC compatibility-replacement and composition rule and the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add `greeting_nfkc(name: str) -> str` to `src/nmg_sdlc_smoke/greet.py`, returning `unicodedata.normalize("NFKC", greet(name))` | Must |
| FR2 | Raise `greet`'s `ValueError("name must not be blank")` for empty, whitespace-only, and non-string names | Must |
| FR3 | Re-export `greeting_nfkc` from `src/nmg_sdlc_smoke/__init__.py` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document `greeting_nfkc` in the README Library section (import list, usage example, behavior sentence) consistent with `greeting_nfc` and `greeting_nfd` | Should |

## Out of Scope

- An NFKD helper, or a configurable normalization-form parameter
- Changes to `greet`, `greeting_nfc`, `greeting_nfd`, or the other existing helpers
- A new `nmg-smoke` CLI flag or option for normalized output

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #356 | 2026-11-23 | Initial feature spec |
