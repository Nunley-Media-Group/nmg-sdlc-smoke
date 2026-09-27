# Requirements: Add nmg-smoke --lowercase flag

**Issue**: #188
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/43-add-nmg-smoke-uppercase-flag/

## User Story

**As a** maintainer running the `nmg-smoke` console script
**I want** a `--lowercase` flag that lowercases the greeting
**So that** I can get `hello, ada` output alongside the existing formatting options

## Background

`nmg-smoke` can uppercase its greeting with `--uppercase` but has no lowercase counterpart. `src/nmg_sdlc_smoke/cli.py` builds an argparse parser with `--uppercase`, `--repeat COUNT`, `--prefix TEXT`, `--no-newline`, `--parentheses`, `--braces`, and `--quotes`. Rendering order is: `greet(name)` → optional `str.upper()` → prefix → parentheses → braces → quotes → repetition and newline handling. Invalid names exit 1 with `nmg-smoke: error: name must not be blank` and no stdout.

The new flag mirrors `--uppercase`: it transforms only the greeting produced by `greet`, before prefix text and wrapper flags are applied, and cannot be combined with `--uppercase`.

## Acceptance Criteria

### AC1: Lowercase the greeting

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --lowercase Ada`
**Then** stdout is exactly `hello, ada` followed by one newline, stderr is empty, and the exit status is 0

### AC2: Compose with existing formatting options

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --lowercase --prefix 'OK: ' --parentheses --repeat 2 --no-newline ADA`
**Then** stdout is exactly `(OK: hello, ada)` LF `(OK: hello, ada)` with no final newline, the prefix text is not lowercased, and the exit status is 0

### AC3: Use Python str.lower semantics for non-ASCII names

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --lowercase ÅSA` and `nmg-smoke --lowercase Straße`
**Then** stdout is exactly `hello, åsa` and `hello, straße` respectively, each followed by one newline, and each exit status is 0

### AC4: Reject combining --lowercase with --uppercase

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --uppercase --lowercase Ada` or `nmg-smoke --lowercase --uppercase Ada`
**Then** the exit status is 2, stderr contains `not allowed with argument`, and stdout is empty

### AC5: Preserve invalid-name handling

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --lowercase " "`
**Then** the exit status is 1, stderr contains `nmg-smoke: error: name must not be blank`, and stdout is empty

### AC6: Preserve default output and document the flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke Ada`, `nmg-smoke --uppercase Ada`, or `nmg-smoke --help`
**Then** the first two print exactly `Hello, Ada` and `HELLO, ADA` each followed by one newline, and `--help` output lists `--lowercase`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | `nmg-smoke` accepts an optional long-only boolean `--lowercase` flag that applies `str.lower()` to the greeting returned by `greet(name)`. | Must |
| FR2 | Lowercasing happens at the same stage as `--uppercase`: before `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, and `--no-newline` processing; prefix text is never lowercased. | Must |
| FR3 | `--lowercase` and `--uppercase` are mutually exclusive; supplying both, in either order, exits 2 with an argparse usage error on stderr and no stdout. | Must |
| FR4 | Output without `--lowercase` is byte-identical to current behavior. | Must |
| FR5 | README CLI section documents `--lowercase` with an example and the mutual exclusion with `--uppercase`. | Must |

## Out of Scope

- Library API changes, including `greet` and `greeting_casefold`
- Lowercasing `--prefix` text or wrapper characters
- Casefold-based (`str.casefold()`) lowercasing
- Changes to any other CLI flag's behavior

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #188 | 2026-09-27 | Initial feature spec |
