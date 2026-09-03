# Requirements: Add greeting_ends_with_name library helper

**Issue**: #71
**Date**: 2026-09-03
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** a public `greeting_ends_with_name(name)` library helper
**So that** callers can observe whether the generated greeting ends with the supplied name while retaining the existing greeting and CLI contracts

---

## Background

The smoke host exposes a pure `greet(name)` function and derived public library helpers in `src/nmg_sdlc_smoke/greet.py`. A suffix predicate adds one independently observable library contract while keeping `greet` as the authority for greeting generation and input validation.

The helper must return the Python boolean produced by `greet(name).endswith(name)` for the same supplied name. The contract is that relationship, not a hardcoded promise that every future greeting format returns `True`.

`greet("Ada")` returns `Hello, Ada` and rejects blank, whitespace-only, and non-string names with `ValueError("name must not be blank")`. Existing derived helpers reuse that validation. `greeting_starts_with_hello(name)` in issue #68 (`specs/68-add-greeting-starts-with-hello-library-function/`) is the nearest public boolean-helper pattern with unit and pytest-bdd coverage. Issue #62 (`specs/62-add-greeting-contains-name-library-function/`) is a neighboring name-membership contract and is not a blocker.

The package has no `greeting_ends_with_name` symbol or export today. Current public `__all__` is `greet`, `greet_many`, `greeting_bytes`, `greeting_is_ascii`, `greeting_length`, `greeting_starts_with_hello`. The `nmg-smoke` CLI in `src/nmg_sdlc_smoke/cli.py` calls `greet` directly. README Library usage is separate from CLI documentation. Root `VERSION` is `3.24.0`. Project metadata declares no runtime dependencies.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: A valid name returns the greeting suffix result

**Given** the installed package is importable
**When** `greeting_ends_with_name("Ada")` is called from the public package
**Then** it returns the Python boolean `True`
**And** the value equals `greet("Ada").endswith("Ada")`

### AC2: A different valid name uses that same name

**Given** the installed package is importable
**When** `greeting_ends_with_name("Jo")` is called from the public package
**Then** it returns the Python boolean `True`
**And** the value equals `greet("Jo").endswith("Jo")`
**And** the result is not specific to the `Ada` example

### AC3: Invalid names preserve greet validation

**Given** `greeting_ends_with_name` is imported from the public package
**When** it is called with a blank, whitespace-only, or non-string name
**Then** it raises `ValueError` with the exact message `name must not be blank`
**And** the error remains the existing `greet` validation error rather than a wrapped or renamed error

### AC4: Existing greeting and CLI behavior remains unchanged

**Given** the distribution is installed
**When** `greet("Ada")` is called and `nmg-smoke Ada` is run
**Then** `greet("Ada")` still returns `Hello, Ada`
**And** the CLI still exits `0`, writes exactly `Hello, Ada` followed by one newline to stdout, and writes nothing to stderr
**And** invalid names retain the existing library and CLI failure behavior

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Provide public `greeting_ends_with_name(name: str) -> bool` behavior equal to `greet(name).endswith(name)` for the same supplied name. | Must | Implement as `return greet(name).endswith(name)`; do not `return True`; do not call `name.endswith(name)` without `greet` |
| FR2 | Make `greeting_ends_with_name` importable from `nmg_sdlc_smoke` without removing or changing any existing public export. | Must | Append to `__all__`; keep `greet`, `greet_many`, `greeting_bytes`, `greeting_is_ascii`, `greeting_length`, `greeting_starts_with_hello` |
| FR3 | Preserve the exact `greet` validation behavior for blank, whitespace-only, and non-string names. | Must | Do not re-validate `name` inside `greeting_ends_with_name`; do not catch, wrap, or rename `ValueError` |
| FR4 | Preserve all existing `greet` and `nmg-smoke` behavior, including current stdout, stderr, and exit status contracts. | Must | Do not edit `cli.py` or the `greet` body |
| FR5 | Add pytest unit coverage and pytest-bdd Gherkin coverage for the acceptance criteria. | Must | Unit in `tests/test_greet.py`; feature `tests/features/add_greeting_ends_with_name_library_helper.feature` |
| FR6 | Update only the README Library usage to import and demonstrate `greeting_ends_with_name`; leave CLI documentation unchanged. | Must | Example `greeting_ends_with_name("Ada")` → `True` |
| FR7 | Add no runtime dependency and leave root `VERSION` unchanged at `3.24.0`. | Must | `str.endswith` is stdlib |

---

## Out of Scope

- Changing the `greet` signature, greeting format, or validation contract
- Adding or changing CLI options, arguments, output, errors, or exit statuses
- Adding a configurable suffix, normalization, or case-insensitive comparison
- Changing runtime dependency metadata or bumping `VERSION`
- Editing README sections outside Library usage
- Adding database, HTTP API, UI, publication, or framework work

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #71 | 2026-09-03 | Initial feature spec |
