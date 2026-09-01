# Requirements: Add nmg-smoke --repeat COUNT option

**Issue**: #45
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** `nmg-smoke --repeat COUNT` to print the existing one-name greeting exactly COUNT times, one line per greeting
**So that** CLI output volume is observable without changing the library `greet` API

---

## Background

The smoke host is a minimal installable Python distribution whose observable CLI success path is a single greeting line. Maintainers need a long option that repeats that same greeting a caller-chosen number of times so volume and line-oriented output can be exercised through the existing console script. The library greeting contract stays a single-name function; this issue does not add a library repeat helper and does not change `greet`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Repeat greeting COUNT times

**Given** the distribution is installed with its console script
**When** `nmg-smoke --repeat 3 Ada` is run
**Then** the process exits 0
**And** stdout is exactly three lines of `Hello, Ada`, each followed by a newline
**And** stderr is empty

### AC2: Omitting --repeat keeps single-line output

**Given** the distribution is installed with its console script
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline

### AC3: Invalid COUNT is rejected

**Given** the distribution is installed with its console script
**When** `nmg-smoke --repeat` is run with a missing COUNT, a non-integer COUNT, `0`, or a negative COUNT
**Then** the process exits non-zero
**And** stdout contains no greeting
**And** stderr contains argparse-style usage or error text

### AC4: Library greet API is unchanged

**Given** a caller imports `greet` from `nmg_sdlc_smoke`
**When** `greet("Ada")` is called
**Then** it returns `Hello, Ada`
**And** blank, whitespace-only, and non-string names still raise `ValueError("name must not be blank")`

### AC5: Blank name is still rejected when --repeat is present

**Given** a blank or whitespace-only name
**When** `nmg-smoke --repeat 2` is invoked with that name
**Then** the CLI exits non-zero without printing a greeting

### AC6: Positional name remains required with --repeat

**Given** the distribution is installed
**When** `nmg-smoke --repeat 2` is run with no name
**Then** the process exits non-zero and does not print a greeting

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `nmg-smoke --repeat COUNT NAME` prints the existing greeting exactly COUNT times, one line per greeting, and exits 0 | Must | Call `greet` once; print that string COUNT times |
| FR2 | Omitting `--repeat` leaves the current single-line greeting unchanged | Must | `nmg-smoke Ada` → `Hello, Ada\n` |
| FR3 | COUNT must be a positive integer; missing COUNT, non-integers, `0`, and negatives exit non-zero with argparse-style stderr and no stdout greeting | Must | argparse `SystemExit`, not the greet `ValueError` path |
| FR4 | Keep the library `greet` API unchanged | Must | No repeat helper; no new parameter |
| FR5 | Long option only (`--repeat`); do not add `-r` | Must | |
| FR6 | `--repeat` does not make the positional name optional | Must | |
| FR7 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR8 | Keep zero runtime dependencies | Must | |
| FR9 | `--repeat 1 NAME` prints the same single greeting line as omitting `--repeat` | Must | COUNT default is 1 |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Adding a library repeat helper or changing `greet_many`
- Adding short option `-r`
- Implementing or changing `nmg-smoke --version`
- Implementing or changing `nmg-smoke --uppercase`
- Multi-name CLI arguments
- Database, HTTP API, UI, or publication pipeline work
- Adding runtime dependencies
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #45 | 2026-09-01 | Initial feature spec |
