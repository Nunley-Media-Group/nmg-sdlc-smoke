# Requirements: Add nmg-smoke --uppercase flag

**Issue**: #43
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** `nmg-smoke --uppercase` to print the existing greeting in uppercase
**So that** the CLI can present an all-caps greeting line without changing the library `greet` API

---

## Background

The smoke host already prints one greeting line from a required positional name. Maintainers need an opt-in long flag that uppercases that same successful greeting line. Without the flag, current CLI output stays exactly as it is today. The library `greet(name)` contract stays `Hello, {name}` with the existing blank-name `ValueError`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Uppercase greeting happy path

**Given** the distribution is installed with its console script
**When** `nmg-smoke --uppercase Ada` is run
**Then** the process exits 0 and prints `HELLO, ADA` followed by a single newline
**And** `nmg-smoke Ada --uppercase` produces the same stdout and exit code

### AC2: Greeting without the flag is unchanged

**Given** the distribution is installed with its console script
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline

### AC3: Flag without a name still fails

**Given** the distribution is installed
**When** `nmg-smoke --uppercase` is run with no name argument
**Then** the process exits non-zero and does not print a greeting

### AC4: Blank name with the flag still fails

**Given** a blank or whitespace-only name
**When** `nmg-smoke --uppercase` is invoked with that name
**Then** the CLI exits non-zero without printing a greeting to stdout

### AC5: Library greet API is unchanged

**Given** the library is importable
**When** `greet("Ada")` is called
**Then** it returns `Hello, Ada`
**And** blank, whitespace-only, and non-string names still raise `ValueError("name must not be blank")`

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `nmg-smoke --uppercase NAME` prints the existing greeting line in uppercase plus one newline and exits 0 | Must | Full line: `HELLO, ADA` for name `Ada`, not name-only |
| FR2 | `nmg-smoke NAME` without `--uppercase` still prints `Hello, NAME` plus one newline and exits 0 | Must | |
| FR3 | `greet(name)` return values and `ValueError("name must not be blank")` stay unchanged | Must | No new library parameter |
| FR4 | `--uppercase` does not make the name optional; missing name still fails with no greeting | Must | |
| FR5 | Blank or whitespace-only name with `--uppercase` still exits non-zero with no stdout greeting | Must | |
| FR6 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR7 | Keep zero runtime dependencies; long option `--uppercase` only (no short `-u`) | Must | |
| FR8 | README CLI documents `--uppercase` without changing the library section | Should | Keep `nmg-smoke Ada` → `Hello, Ada` |

---

## Out of Scope

- Changing `greet` (no new parameter, no uppercase in the library)
- `greet_many` or other library exports
- Short `-u`
- `--version` behavior
- Database, HTTP API, UI, or publication pipeline
- New runtime dependencies
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #43 | 2026-09-01 | Initial feature spec |
