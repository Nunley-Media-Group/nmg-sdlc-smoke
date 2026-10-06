# Requirements: Add nmg-smoke --casefold flag

**Issue**: #197
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/194-add-nmg-smoke-titlecase-flag/

## User Story

**As a** maintainer running the `nmg-smoke` console script
**I want** a `--casefold` flag that applies Unicode casefolding to the greeting
**So that** I get caseless-comparison output such as `hello, strasse` from any input casing alongside the existing case and formatting options

## Background

`src/nmg_sdlc_smoke/cli.py` builds an argparse parser with a mutually exclusive `case` group containing `--uppercase`, `--lowercase`, `--swapcase`, and `--titlecase`, plus `--repeat COUNT`, `--prefix TEXT`, `--no-newline`, `--parentheses`, `--braces`, and `--quotes`, and a required `name` positional. Rendering order is: `greet(name)` → optional `str.upper()` / `str.lower()` / `str.swapcase()` / `str.title()` → prefix → parentheses → braces → quotes → repetition and newline handling. Invalid names exit 1 with `nmg-smoke: error: name must not be blank` and no stdout. `--lowercase` uses `str.lower()`, which leaves characters such as `ß` unchanged. The library exposes `greeting_casefold(name)`, but the CLI has no casefold option.

The new flag transforms only the greeting produced by `greet(name)` at the same stage as the existing case flags, before prefix text and wrapper flags are applied, and cannot be combined with another case flag.

## Acceptance Criteria

### AC1: Casefold the greeting

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --casefold Straße`
**Then** stdout is exactly `hello, strasse` followed by one newline, stderr is empty, and the exit status is 0

### AC2: Use Python str.casefold semantics

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --casefold ADA` and `nmg-smoke --casefold ΣΊΣΥΦΟΣ`
**Then** stdout is exactly `hello, ada` and `hello, σίσυφοσ` respectively, each followed by one newline, and each exit status is 0

### AC3: Compose with existing formatting options

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --casefold --prefix 'OK: ' --quotes --repeat 2 --no-newline Straße`
**Then** stdout is exactly `"OK: hello, strasse"` LF `"OK: hello, strasse"` with no final newline, the prefix text keeps its original case, and the exit status is 0

### AC4: Reject combining --casefold with another case flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --casefold --uppercase Ada`, `nmg-smoke --uppercase --casefold Ada`, `nmg-smoke --casefold --lowercase Ada`, `nmg-smoke --lowercase --casefold Ada`, `nmg-smoke --casefold --swapcase Ada`, `nmg-smoke --swapcase --casefold Ada`, `nmg-smoke --casefold --titlecase Ada`, or `nmg-smoke --titlecase --casefold Ada`
**Then** each exit status is 2, stderr contains `not allowed with argument`, and stdout is empty

### AC5: Preserve invalid-name handling

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --casefold " "`
**Then** the exit status is 1, stderr contains `nmg-smoke: error: name must not be blank`, and stdout is empty

### AC6: Preserve existing output and document the flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke Ada`, `nmg-smoke --lowercase Straße`, or `nmg-smoke --help`
**Then** the first two print exactly `Hello, Ada` and `hello, straße` each followed by one newline, and `--help` output lists `--casefold`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | `nmg-smoke` accepts an optional long-only boolean `--casefold` flag that applies `str.casefold()` to the greeting returned by `greet(name)`. | Must |
| FR2 | Casefolding happens at the same stage as `--uppercase`, `--lowercase`, `--swapcase`, and `--titlecase`: before `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, and `--no-newline` processing; prefix text and wrapper characters are never casefolded. | Must |
| FR3 | `--casefold` belongs to the same mutually exclusive group as `--uppercase`, `--lowercase`, `--swapcase`, and `--titlecase`; combining it with any of them, in any order, exits 2 with an argparse usage error on stderr and no stdout. | Must |
| FR4 | Output without `--casefold` is byte-identical to current behavior. | Must |
| FR5 | The README CLI section documents `--casefold` with a console example, its `str.casefold()` semantics, and its mutual exclusion with the other case flags. | Must |

## Out of Scope

- Library API changes, including `greet` and `greeting_casefold`
- Casefolding `--prefix` text or wrapper characters
- Locale-aware or custom case mapping beyond Python `str.casefold()`
- Changes to any other CLI flag's behavior

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #197 | 2026-10-06 | Initial feature spec |
