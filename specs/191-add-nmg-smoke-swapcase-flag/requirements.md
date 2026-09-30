# Requirements: Add nmg-smoke --swapcase flag

**Issue**: #191
**Date**: 2026-09-30
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/188-add-nmg-smoke-lowercase-flag/

## User Story

**As a** maintainer running the `nmg-smoke` console script
**I want** a `--swapcase` flag that inverts the letter case of the greeting
**So that** I can get `hELLO, aDA` output alongside the existing case and formatting options

## Background

`src/nmg_sdlc_smoke/cli.py` builds an argparse parser with a mutually exclusive `case` group containing `--uppercase` and `--lowercase`, plus `--repeat COUNT`, `--prefix TEXT`, `--no-newline`, `--parentheses`, `--braces`, and `--quotes`, and a required `name` positional. Rendering order is: `greet(name)` → optional `str.upper()` / `str.lower()` → prefix → parentheses → braces → quotes → repetition and newline handling. Invalid names exit 1 with `nmg-smoke: error: name must not be blank` and no stdout. No swapcase behavior exists in the CLI or library.

The new flag transforms only the greeting produced by `greet(name)` at the same stage as the existing case flags, before prefix text and wrapper flags are applied, and cannot be combined with another case flag.

## Acceptance Criteria

### AC1: Swap the case of the greeting

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --swapcase Ada`
**Then** stdout is exactly `hELLO, aDA` followed by one newline, stderr is empty, and the exit status is 0

### AC2: Compose with existing formatting options

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --swapcase --prefix 'OK: ' --parentheses --repeat 2 --no-newline ADA`
**Then** stdout is exactly `(OK: hELLO, ada)` LF `(OK: hELLO, ada)` with no final newline, the prefix text keeps its original case, and the exit status is 0

### AC3: Use Python str.swapcase semantics for non-ASCII names

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --swapcase ÅSA` and `nmg-smoke --swapcase Straße`
**Then** stdout is exactly `hELLO, åsa` and `hELLO, sTRASSE` respectively, each followed by one newline, and each exit status is 0

### AC4: Reject combining --swapcase with another case flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --swapcase --uppercase Ada`, `nmg-smoke --uppercase --swapcase Ada`, `nmg-smoke --swapcase --lowercase Ada`, or `nmg-smoke --lowercase --swapcase Ada`
**Then** each exit status is 2, stderr contains `not allowed with argument`, and stdout is empty

### AC5: Preserve invalid-name handling

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke --swapcase " "`
**Then** the exit status is 1, stderr contains `nmg-smoke: error: name must not be blank`, and stdout is empty

### AC6: Preserve existing output and document the flag

**Given** the installed `nmg-smoke` console script
**When** the user runs `nmg-smoke Ada`, `nmg-smoke --uppercase Ada`, `nmg-smoke --lowercase Ada`, or `nmg-smoke --help`
**Then** the first three print exactly `Hello, Ada`, `HELLO, ADA`, and `hello, ada` each followed by one newline, and `--help` output lists `--swapcase`

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | `nmg-smoke` accepts an optional long-only boolean `--swapcase` flag that applies `str.swapcase()` to the greeting returned by `greet(name)`. | Must |
| FR2 | Case swapping happens at the same stage as `--uppercase` and `--lowercase`: before `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, and `--no-newline` processing; prefix text and wrapper characters are never case-swapped. | Must |
| FR3 | `--swapcase` belongs to the same mutually exclusive group as `--uppercase` and `--lowercase`; combining it with either, in any order, exits 2 with an argparse usage error on stderr and no stdout. | Must |
| FR4 | Output without `--swapcase` is byte-identical to current behavior. | Must |
| FR5 | The README CLI section documents `--swapcase` with an example and its mutual exclusion with `--uppercase` and `--lowercase`. | Must |

## Out of Scope

- Library API changes, including `greet` and `greeting_casefold`
- Case-swapping `--prefix` text or wrapper characters
- Title-casing or any other new case transformation
- Changes to any other CLI flag's behavior

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #191 | 2026-09-30 | Initial feature spec |
