# Requirements: Add nmg-smoke --separator TEXT option

**Issue**: #98
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** `nmg-smoke --separator TEXT` to control the text between repeated rendered greetings
**So that** a registered smoke queue for nmg-sdlc #374 can observe one minimal new CLI option without changing greeting, prefix, uppercase, name, or error behavior

---

## Background

This issue is a disposable verification fixture for Nunley-Media-Group/nmg-sdlc issue 374, whose approved spec is published by PR 376. The fixture adds one optional long option to the existing `nmg-smoke` console script: `--separator TEXT` controls only the text inserted between repeated rendered greetings.

The default between-greeting text remains a newline. The final terminator newline remains governed by existing `--no-newline`. Prefix, uppercase, positional name, and error behavior stay unchanged. Python consumer details belong only in this disposable host and must not be copied into reusable nmg-sdlc defaults. The link to nmg-sdlc #374 is explanatory fixture scope, not a GitHub blocked-by relationship. Official GitHub `blockedBy` edges for #98 are empty; do not add generated dependency fields.

Exactly two Gherkin scenarios are authorized (AC1 and AC2). Do not add further acceptance scenarios.

`nmg-smoke` already accepts `--uppercase`, `--repeat COUNT` (positive integer, default 1), `--prefix TEXT`, `--no-newline`, and a required positional name. It does not accept `--separator`.

Observable success output today:

- `nmg-smoke Ada` prints `Hello, Ada` followed by a single newline
- `nmg-smoke --repeat 2 Ada` prints two lines of `Hello, Ada`, each followed by a newline
- `--no-newline` omits only the final terminator; repeated greetings still use newline between them
- `--prefix` prepends TEXT after any uppercase transform; blank or missing names still fail with no stdout greeting

`greet("Ada")` returns `Hello, Ada`. Blank, whitespace-only, and non-string names still raise `ValueError("name must not be blank")`. Neighboring delivered CLI contracts are issues #43, #45, #52, and #58. Stopped issue #96 is a different 372-delivery fixture and is not this work.

Issue-body “do not bump VERSION” applies to authoring and feature-implementation tasks only. Delivery/open-pr still must perform the normal enhancement minor bump required by `CHANGELOG.md` and `steering/snippets/project-tech.md`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario. Authorize only these two.

### AC1: Repeat 2 with an explicit separator keeps the final newline

**Given** the distribution is installed with its console script
**When** `nmg-smoke --repeat 2 --separator ' | ' Ada` is run
**Then** the process exits 0
**And** stdout is exactly `Hello, Ada | Hello, Ada` followed by a single newline
**And** stderr is empty

### AC2: Omitting --separator preserves current repeated lines

**Given** the distribution is installed with its console script
**When** `nmg-smoke --repeat 2 Ada` is run
**Then** the process exits 0
**And** stdout is exactly two lines of `Hello, Ada`, each followed by a newline
**And** stderr is empty

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `nmg-smoke --repeat 2 --separator ' | ' Ada` prints exactly `Hello, Ada | Hello, Ada` plus one final newline, exits 0, and writes nothing to stderr | Must | TEXT is space-pipe-space |
| FR2 | Omitting `--separator` leaves `nmg-smoke --repeat 2 Ada` as two newline-terminated `Hello, Ada` lines | Must | Matches #45 two-line output |
| FR3 | Cover AC1 and AC2 only; do not add further Gherkin scenarios | Must | No missing-TEXT, empty TEXT, `--repeat 1`, flag-order, uppercase, prefix, `--no-newline` composition, or error-path scenarios |
| FR4 | `--separator` is a long option that takes TEXT; default between-repeat text is a newline | Must | No short option |
| FR5 | Existing `--no-newline` still governs only the final terminator newline | Must | Not an extra Gherkin scenario |
| FR6 | `--uppercase`, `--prefix`, name validation, and error paths stay unchanged | Must | No library API change |
| FR7 | Keep zero runtime dependencies | Must | argparse and `print` only |
| FR8 | Feature-implementation tasks must not edit `VERSION` or `CHANGELOG.md`; delivery/open-pr must apply the normal enhancement minor bump `3.32.0` → `3.33.0` with a `#98` CHANGELOG entry and dynamic `pyproject.toml` VERSION read | Must | Do not write `**Version bump**: major` |
| FR9 | Cover AC1 and AC2 with pytest unit tests and pytest-bdd under `tests/features/` | Must | |
| FR10 | README CLI documentation describes `--separator` | Should | Library section unchanged |

---

## Out of Scope

- Changing `greet` or any other library API, export, or validation message
- Changing `--uppercase`, `--prefix TEXT`, `--repeat COUNT` validity rules, the required positional name, or blank-name errors
- Changing `--no-newline` semantics (it still governs only the final terminator newline)
- Adding a short option for separator
- Additional Gherkin scenarios beyond AC1 and AC2, including missing-TEXT, empty TEXT, `--repeat 1`, flag-order, uppercase, prefix, and error-path scenarios
- Replaying, editing, or replacing stopped issue #96
- Database, HTTP API, UI, publication pipeline, or runtime dependencies
- Copying this Python CLI shape into reusable nmg-sdlc defaults
- Skipping the delivery-owned minor VERSION/CHANGELOG bump
- Implementing this fixture during write-spec; registered-provider smoke runs later

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #98 | 2026-09-07 | Initial feature spec |
