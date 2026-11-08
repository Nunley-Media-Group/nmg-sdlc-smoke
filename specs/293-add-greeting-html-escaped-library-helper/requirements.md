# Requirements: Add greeting_html_escaped library helper

**Issue**: #293
**Date**: 2026-11-08
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/217-add-greeting-url-encoded-library-helper/

## User Story

**As a** caller of the Python greeting library
**I want** a public `greeting_html_escaped(name)` helper that returns the HTML-escaped completed greeting
**So that** I can embed a greeting in HTML text or attribute values without re-implementing the greeting or its escaping

## Background

For valid names, `greet(name)` returns `Hello, {name}`. For empty, whitespace-only, and non-string names, it raises `ValueError("name must not be blank")`.

The helper escapes the complete greeting, including the `Hello, ` prefix, with Python's standard-library `html.escape(...)` and its default `quote=True`: `&` → `&amp;`, `<` → `&lt;`, `>` → `&gt;`, `"` → `&quot;`, and `'` → `&#x27;`. All other characters, including non-ASCII characters, are returned unchanged. No Unicode normalization is applied.

Each public helper has four parts:
- a definition in `src/nmg_sdlc_smoke/greet.py`
- a self-aliased re-export from `nmg_sdlc_smoke`
- an entry in `nmg_sdlc_smoke.__all__`
- a README Library entry with an import, an example result, and a prose contract line

`greeting_url_encoded` already returns a percent-encoded greeting. No existing helper returns an HTML-escaped greeting.

## Acceptance Criteria

### AC1: Return the greeting unchanged when no HTML-special characters are present

**Given** the valid names `Ada` and `Zoë` (with precomposed U+00EB)
**When** a caller invokes `greeting_html_escaped` with each name
**Then** it returns the `str` `Hello, Ada` for `Ada` and `Hello, Zoë` for `Zoë`

### AC2: Escape HTML-special characters in the greeting

**Given** the valid names `<Ada & Bo>` and `O'Brien "Jr"`
**When** a caller invokes `greeting_html_escaped` with each name
**Then** it returns `Hello, &lt;Ada &amp; Bo&gt;` for `<Ada & Bo>` and `Hello, O&#x27;Brien &quot;Jr&quot;` for `O'Brien "Jr"`, each equal to `html.escape(greet(name))`

### AC3: Preserve invalid-name behavior

**Given** the invalid names `""`, `" \t"`, `None`, and `42`
**When** a caller invokes `greeting_html_escaped` with each name
**Then** each call raises `ValueError("name must not be blank")`, as `greet` does, and returns no value

### AC4: Expose and document the helper without changing existing surfaces

**Given** the installed `nmg_sdlc_smoke` package and the README Library section
**When** a caller imports `greeting_html_escaped` from `nmg_sdlc_smoke`, follows the README example, and runs `nmg-smoke Ada`
**Then** `greeting_html_escaped("<Ada & Bo>")` returns `Hello, &lt;Ada &amp; Bo&gt;`
**And** `"greeting_html_escaped"` appears in `nmg_sdlc_smoke.__all__` alongside every previously listed name
**And** `nmg-smoke Ada` still prints exactly `Hello, Ada` with one trailing newline and exits with status 0
**And** the README documents three things:
- that the result is `html.escape` with its default `quote=True` (escaping `&`, `<`, `>`, `"`, and `'`)
- that the escaping covers the complete greeting, including the `Hello, ` prefix
- the inherited `ValueError("name must not be blank")`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add pure `greeting_html_escaped(name: str) -> str` returning `html.escape(greet(name))` with default `quote=True` | Must |
| FR2 | Propagate `greet`'s `ValueError("name must not be blank")` unchanged for invalid names | Must |
| FR3 | Export `greeting_html_escaped` from `nmg_sdlc_smoke` with a self-alias and list it in `__all__` without removing existing exports | Must |
| FR4 | Document the helper in the README Library section with an import, an example, and a prose contract line | Must |
| FR5 | Leave `greet`, existing helpers, and `nmg-smoke` output unchanged | Must |

## Out of Scope

- A `nmg-smoke` CLI flag or option that prints the HTML-escaped greeting
- Unescaping HTML back to a greeting
- `quote=False` mode, named-entity encoding of non-ASCII characters, or HTML templating
- Unicode normalization of names
- Changes to `greeting_url_encoded` or any other existing helper

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #293 | 2026-11-08 | Initial feature spec |
