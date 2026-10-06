# Requirements: Add nmg-smoke --titlecase flag

**Issue**: #194
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/191-add-nmg-smoke-swapcase-flag/

## User Story

**As a** maintainer running the `nmg-smoke` console script
**I want** a `--titlecase` flag that title-cases the greeting
**So that** I can get `Hello, Ada Lovelace` output from any input casing alongside the existing case and formatting options

## Background

`src/nmg_sdlc_smoke/cli.py` builds an argparse parser with a mutually exclusive `case` group containing `--uppercase`, `--lowercase`, and `--swapcase`, plus `--repeat COUNT`, `--prefix TEXT`, `--no-newline`, `--parentheses`, `--braces`, and `--quotes`, and a required `name` positional. Rendering order is: `greet(name)` → optional `str.upper()` / `str.lower()` / `str.swapcase()` → prefix → parentheses → braces → quotes → repetition and newline handling. Invalid names exit 1 with `nmg-smoke: error: name must not be blank` and no stdout. No title-casing behavior exists in the CLI or library.

The new flag transforms only the greeting produced by `greet(name)` at the same stage as the existing case flags, before prefix text and wrapper flags are applied, and cannot be combined with another case flag.

## Acceptance Criteria

### AC1: Title-case the greeting

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --titlecase ada`
**Then** stdout is exactly `Hello, Ada` followed by one newline, stderr is empty, and the exit status is 0

### AC2: Use Python str.title semantics for multi-word, uppercase, and punctuated names

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --titlecase "ADA LOVELACE"`, `nmg-smoke --titlecase "o'neil"`, and `nmg-smoke --titlecase åsa`
**Then** stdout is exactly `Hello, Ada Lovelace`, `Hello, O'Neil`, and `Hello, Åsa` respectively, each followed by one newline, and each exit status is 0

### AC3: Compose with existing formatting options

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --titlecase --prefix 'ok: ' --quotes --repeat 2 --no-newline ADA`
**Then** stdout is exactly `"ok: Hello, Ada"` LF `"ok: Hello, Ada"` with no final newline, the prefix text keeps its original case, and the exit status is 0

### AC4: Reject combining --titlecase with another case flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --titlecase --uppercase Ada`, `nmg-smoke --uppercase --titlecase Ada`, `nmg-smoke --titlecase --lowercase Ada`, `nmg-smoke --lowercase --titlecase Ada`, `nmg-smoke --titlecase --swapcase Ada`, or `nmg-smoke --swapcase --titlecase Ada`
**Then** each exit status is 2, stderr contains `not allowed with argument`, and stdout is empty

### AC5: Preserve invalid-name handling

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --titlecase " "`
**Then** the exit status is 1, stderr contains `nmg-smoke: error: name must not be blank`, and stdout is empty

### AC6: Preserve existing output and document the flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke Ada`, `nmg-smoke --uppercase Ada`, `nmg-smoke --lowercase Ada`, `nmg-smoke --swapcase Ada`, or `nmg-smoke --help`
**Then** the first four print exactly `Hello, Ada`, `HELLO, ADA`, `hello, ada`, and `hELLO, aDA` each followed by one newline, and `--help` output lists `--titlecase`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | `nmg-smoke` accepts an optional long-only boolean `--titlecase` flag that applies `str.title()` to the greeting returned by `greet(name)`. | Must |
| FR2 | Title-casing happens at the same stage as `--uppercase`, `--lowercase`, and `--swapcase`: before `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, and `--no-newline` processing; prefix text and wrapper characters are never title-cased. | Must |
| FR3 | `--titlecase` belongs to the same mutually exclusive group as `--uppercase`, `--lowercase`, and `--swapcase`; combining it with any of them, in any order, exits 2 with an argparse usage error on stderr and no stdout. | Must |
| FR4 | Output without `--titlecase` is byte-identical to current behavior. | Must |
| FR5 | The README CLI section documents `--titlecase` with a console example, its `str.title()` semantics, and its mutual exclusion with the other case flags. | Must |

## Out of Scope

- Library API changes, including `greet` and `greeting_casefold`
- Title-casing `--prefix` text or wrapper characters
- Apostrophe-aware, locale-aware, or otherwise custom title-casing beyond Python `str.title()`
- Changes to any other CLI flag's behavior

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #194 | 2026-10-06 | Initial feature spec |
