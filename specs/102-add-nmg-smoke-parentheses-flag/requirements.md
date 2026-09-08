# Requirements: Add nmg-smoke parentheses flag

**Issue**: #102
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer using the Python smoke CLI
**I want** a boolean `--parentheses` option
**So that** each fully composed greeting can be enclosed in literal parentheses without changing existing output by default.

## Background

Add one small opt-in formatting capability. Wrap the fully composed greeting after existing uppercase and prefix transforms and before repeat/newline output. Do not escape or otherwise transform content.

## Current State

The CLI supports uppercase, prefix, repeat, and final-newline suppression. Uppercase applies to the greeting before the literal prefix is added; repeat and newline handling emit the composed message. No library changes are needed.

## Acceptance Criteria

### AC1: Enabled parentheses compose with existing flags

**Given** the CLI is available
**When** `nmg-smoke --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada` runs
**Then** exit status is 0, stderr is empty, and stdout is exactly `(ok: HELLO, ADA)\n(ok: HELLO, ADA)`, where `\n` denotes one LF and there is no final LF.

### AC2: Absent flag preserves composed and default output

**Given** the CLI is available
**When** the same command runs without `--parentheses` and the default command `nmg-smoke Ada` runs
**Then** both exit 0 with empty stderr; stdout is respectively `ok: HELLO, ADA\nok: HELLO, ADA` and `Hello, Ada\n`, byte-identical to existing behavior.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add long-only boolean --parentheses, accepting no value and disabled by default. | Must |
| FR2 | Enclose each fully composed greeting in literal ( and ) after uppercase/prefix and before repeat/newline emission. No escaping or additional content transformation. | Must |
| FR3 | Flag absence preserves existing output bytes; existing validation, library APIs, and other option semantics remain unchanged. | Must |
| FR4 | Exactly two BDD scenarios cover AC1 and AC2; document the new option and preserve released changelog history. | Must |

## Out of Scope

- Library changes, dependencies, new validation, escaping, additional formatting options, or unrelated behavior.
- Work on stopped issues #100, #98, or #96 or other queues.
- Implementation-owned VERSION changes; version selection and release remain delivery-owned on the current major line.


---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #102 | 2026-09-07 | Initial feature spec |
