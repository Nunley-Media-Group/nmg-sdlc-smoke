# Requirements: Add nmg-smoke --prefix TEXT option

**Issue**: #52
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** `nmg-smoke --prefix TEXT` to prepend TEXT to each successful CLI greeting line
**So that** CLI output can carry a caller-chosen prefix without changing the library `greet` API

---

## Background

The smoke host already prints one successful greeting line from a required positional name, optionally uppercased with `--uppercase` and optionally repeated with `--repeat COUNT`. Maintainers need a long option that prepends caller-supplied TEXT to that successful printed line so prefixed output can be exercised through the existing console script. Omitting the option must leave current successful output unchanged. The library `greet(name)` contract stays `Hello, {name}` with the existing blank-name `ValueError`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Prefix successful greeting happy path

**Given** the distribution is installed with its console script
**When** `nmg-smoke --prefix 'OK: ' Ada` is run
**Then** the process exits 0 and prints `OK: Hello, Ada` followed by a single newline
**And** `nmg-smoke Ada --prefix 'OK: '` produces the same stdout and exit code
**And** stderr is empty

### AC2: Omitting --prefix leaves output unchanged

**Given** the distribution is installed with its console script
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline

### AC3: Missing TEXT is rejected

**Given** the distribution is installed with its console script
**When** `nmg-smoke --prefix` is run without a TEXT argument
**Then** the process exits non-zero
**And** stdout contains no greeting
**And** stderr contains argparse-style usage or error text

### AC4: Library greet API is unchanged

**Given** the library is importable
**When** a caller invokes `greet` with `Ada`
**Then** the function returns exactly `Hello, Ada`
**And** blank, whitespace-only, and non-string names still raise `ValueError` with message `name must not be blank`

### AC5: Blank name is still rejected when --prefix is present

**Given** a blank or whitespace-only name
**When** `nmg-smoke --prefix 'OK: '` is invoked with that name
**Then** the CLI exits non-zero without printing a greeting to stdout

### AC6: Positional name remains required with --prefix

**Given** the distribution is installed
**When** `nmg-smoke --prefix 'OK: '` is run with no name argument
**Then** the process exits non-zero and does not print a greeting

### AC7: Prefix applies to each printed line after uppercase

**Given** the distribution is installed with its console script
**When** `nmg-smoke --prefix 'OK: ' --uppercase Ada` is run
**Then** the process exits 0 and prints `OK: HELLO, ADA` followed by a single newline
**And** when `nmg-smoke --prefix 'OK: ' --repeat 2 Ada` is run, stdout is exactly two lines of `OK: Hello, Ada`, each followed by a newline
**And** the supplied TEXT is not itself uppercased

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `nmg-smoke --prefix TEXT NAME` prepends TEXT exactly as supplied (no extra separator) to each successful printed greeting line, then exits 0 | Must | Callers who want a space include it in TEXT (`OK: `) |
| FR2 | Omitting `--prefix` leaves current successful CLI output unchanged | Must | `nmg-smoke Ada` → `Hello, Ada\n` |
| FR3 | `--prefix` without a TEXT argument exits non-zero with argparse-style stderr and no stdout greeting | Must | argparse `SystemExit`, not the greet `ValueError` path |
| FR4 | Keep the library `greet` API unchanged | Must | No prefix parameter; no new library helper |
| FR5 | Long option only (`--prefix`); do not add a short option | Must | No `-p` |
| FR6 | `--prefix` does not make the positional name optional | Must | |
| FR7 | Blank or whitespace-only name with `--prefix` still exits non-zero with no stdout greeting | Must | Existing `parser.exit(1, ...)` path |
| FR8 | TEXT is prepended after any `--uppercase` transformation; `--repeat COUNT` prints that same prefixed line COUNT times; TEXT is not uppercased | Must | `prefix + message` after `message.upper()` |
| FR9 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR10 | Keep zero runtime dependencies | Must | |
| FR11 | README CLI documents `--prefix TEXT` without changing the library section | Should | |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Changing `greeting_length` or other library exports
- Adding a short option such as `-p`
- Changing `--uppercase`, `--repeat`, or `--version` behavior except as the `--prefix` composition in AC7/FR8
- Treating empty TEXT as an error (empty TEXT on a successful name is the same stdout as omitting `--prefix`)
- Multi-name CLI arguments
- Database, HTTP API, UI, or publication pipeline work
- Adding runtime dependencies
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #52 | 2026-09-01 | Initial feature spec |
