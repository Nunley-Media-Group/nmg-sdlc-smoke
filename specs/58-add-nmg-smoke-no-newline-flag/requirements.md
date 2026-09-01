# Requirements: Add nmg-smoke --no-newline flag

**Issue**: #58
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer exercising nmg-sdlc against this disposable Python host
**I want** `nmg-smoke --no-newline` to omit the terminator newline on successful CLI output
**So that** a long boolean CLI flag can be exercised without changing library APIs or failure behavior

---

## Background

The smoke host currently prints each successful greeting followed by a newline. It accepts a required positional name and the long options `--uppercase`, `--repeat COUNT`, and `--prefix TEXT`. Maintainers need an opt-in long boolean flag that preserves greeting text and newlines between repeated greetings while omitting only the final terminator newline. Omitting the flag must leave current successful output unchanged. Library greeting contracts and existing failure paths stay unchanged.

`nmg-smoke Ada` currently writes `Hello, Ada
`. `--repeat 3` writes three newline-terminated greeting lines. `--uppercase` transforms the greeting before printing, and `--prefix TEXT` prepends TEXT after uppercase. Blank or whitespace-only names exit non-zero with no stdout greeting. Missing names and invalid repeat counts remain argparse failures. `greet("Ada")` returns `Hello, Ada`; invalid names raise `ValueError("name must not be blank")`; `greeting_length("Ada")` returns 10.

Neighboring delivered CLI contracts are issue #43 (`--uppercase`), issue #45 (`--repeat COUNT`), and issue #52 (`--prefix TEXT`). This issue changes only the successful stdout terminator and has no blocked-by relationship to those issues.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Omit final newline on success

**Given** the distribution is installed with its console script
**When** `nmg-smoke --no-newline Ada` is run
**Then** the process exits 0
**And** stdout is exactly `Hello, Ada` with no trailing newline
**And** `nmg-smoke Ada --no-newline` produces the same stdout and exit code
**And** stderr is empty

### AC2: Omitting the flag keeps the trailing newline

**Given** the distribution is installed with its console script
**When** `nmg-smoke Ada` is run
**Then** the process exits 0 and prints `Hello, Ada` followed by a single newline

### AC3: Repeated greetings keep separating newlines

**Given** the distribution is installed with its console script
**When** `nmg-smoke --no-newline --repeat 3 Ada` is run
**Then** the process exits 0
**And** stdout is exactly three `Hello, Ada` greetings separated by newlines, with no newline after the last greeting
**And** stderr is empty

### AC4: Uppercase composition still omits only the final newline

**Given** the distribution is installed with its console script
**When** `nmg-smoke --no-newline --uppercase Ada` is run
**Then** the process exits 0
**And** stdout is exactly `HELLO, ADA` with no trailing newline
**And** stderr is empty

### AC5: Flag without a name still fails

**Given** the distribution is installed
**When** `nmg-smoke --no-newline` is run with no name argument
**Then** the process exits non-zero and does not print a greeting

### AC6: Blank name with the flag still fails

**Given** a blank or whitespace-only name
**When** `nmg-smoke --no-newline` is invoked with that name
**Then** the CLI exits non-zero without printing a greeting to stdout

### AC7: Library APIs are unchanged

**Given** a caller imports from `nmg_sdlc_smoke`
**When** `greet("Ada")` and `greeting_length("Ada")` are called
**Then** `greet` returns `Hello, Ada` and `greeting_length` returns 10
**And** blank, whitespace-only, and non-string names still raise `ValueError("name must not be blank")`

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | `nmg-smoke --no-newline NAME` prints the existing successful greeting text and omits only the final terminator newline when one would otherwise be present, then exits 0 | Must | Implement as a long boolean argparse option |
| FR2 | Omitting `--no-newline` leaves current successful CLI output unchanged | Must | `nmg-smoke Ada` remains `Hello, Ada
` |
| FR3 | With `--repeat COUNT` greater than 1, greetings stay separated by newlines and only the last greeting lacks a trailing newline | Must | `--repeat 3 Ada` with the flag yields `Hello, Ada
Hello, Ada
Hello, Ada` |
| FR4 | With `--uppercase`, the printed text is the uppercased greeting and only the final terminator newline is omitted | Must | `HELLO, ADA` with no trailing newline |
| FR5 | The option is long-only (`--no-newline`) and accepts no value | Must | Do not add `-n` or `nargs` |
| FR6 | `--no-newline` does not make the positional name optional | Must | Missing name remains argparse failure |
| FR7 | Blank or whitespace-only names with `--no-newline` still exit non-zero with no stdout greeting | Must | Existing `parser.exit(1, ...)` path |
| FR8 | Keep `greet`, `greeting_length`, package exports, and library validation unchanged | Must | No library parameter or helper for newline control |
| FR9 | `--no-newline --repeat 1 NAME` produces the same stdout and exit code as `--no-newline NAME` | Must | Both omit the sole terminator newline |
| FR10 | Existing `--prefix TEXT` behavior remains unchanged; newline control applies after the already-transformed message is formed | Must | Do not rewrite prefix or uppercase transformation order |
| FR11 | Cover every acceptance criterion with pytest unit tests and pytest-bdd Gherkin under `tests/features/` | Must | |
| FR12 | Keep zero runtime dependencies; `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` pass | Must | Use argparse and `print` only |
| FR13 | README CLI documentation describes `--no-newline`; the library section remains unchanged | Should | |

---

## Out of Scope

- Changing `greet` validation, return format, or signature
- Changing `greeting_length` or other library exports
- Adding a short option such as `-n`
- Making the positional name optional
- Changing `--uppercase`, `--repeat`, `--prefix`, or `--version` semantics beyond composing their successful output with the final-newline choice
- Stripping or rewriting newlines inside greeting text; only the final successful stdout terminator is in scope
- Multi-name CLI arguments
- Database, HTTP API, UI, or publication pipeline work
- Adding runtime dependencies
- Bumping `VERSION`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #58 | 2026-09-01 | Initial feature spec |
