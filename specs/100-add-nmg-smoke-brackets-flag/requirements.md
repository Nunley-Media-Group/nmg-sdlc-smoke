# Requirements: Add nmg-smoke --brackets flag

**Issue**: #100
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer exercising the disposable Python SDLC smoke host
**I want** an optional `--brackets` flag around each fully composed greeting
**So that** one minimal enhancement can exercise the authorized fresh delivery invocation.

## Background

This is one disposable fixture for the explicitly authorized fresh invocation after the provider identity repair in Nunley-Media-Group/nmg-sdlc#374. It is not reusable Python behavior or authorization to retry stopped queues. Issues #98 and #96 remain untouched.

## Current State

The CLI composes a greeting, optionally uppercases the greeting, prepends the literal prefix, then repeats that message with existing newline handling. There is no brackets flag. Existing delivered prefix and no-newline contracts remain unchanged.

## Acceptance Criteria

### AC1: Brackets wrap each fully composed greeting

**Given** the installed nmg-smoke console script
**When** `nmg-smoke --brackets --uppercase --prefix 'ok[]: ' --repeat 2 --no-newline 'Ada[Q]'` runs
**Then** exit status is 0, stderr is empty, and stdout is exactly `[ok[]: HELLO, ADA[Q]]\n[ok[]: HELLO, ADA[Q]]`, where `\n` denotes one LF and there is no final LF.
**And** `nmg-smoke --brackets Ada` writes exactly `[Hello, Ada]\n`, exits 0, and has empty stderr.

### AC2: Omitting brackets preserves default and composed output

**Given** the installed nmg-smoke console script
**When** `nmg-smoke Ada` and `nmg-smoke --uppercase --prefix 'ok[]: ' --repeat 2 --no-newline 'Ada[Q]'` run without `--brackets`
**Then** their stdout is exactly `Hello, Ada\n` and `ok[]: HELLO, ADA[Q]\nok[]: HELLO, ADA[Q]` respectively, with the final LF only in the first output.
**And** each exits 0 with empty stderr.

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add optional long boolean --brackets; wrap each fully composed greeting in literal square brackets after uppercase/prefix and before repeat/newline output. | Must |
| FR2 | Bracketing performs no escaping or further transformation inside its contents, including existing brackets; uppercase still affects only the greeting, not the prefix. | Must |
| FR3 | Omission is byte-identical to current output. Repeat count, separating newlines, final-newline control, validation, and library APIs retain existing semantics. | Must |
| FR4 | Cover AC1 and AC2 with exactly two BDD scenarios; retain Python 3.12+, zero runtime dependencies, and required repository verification. | Must |

## Out of Scope

- Implementing or executing in the authoring clone; this contribution publishes only the approved four-file spec.
- Separator/suffix work, modifications to #98 or #96, additional issues, replacement queues, or unchanged retries.
- New library helpers, configurable delimiters, escaping rules, short flags, or provider/controller changes.


## Release Ownership

The implementation/delivery owner handles any release VERSION update on the current 3.x line. Spec publication leaves VERSION untouched.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #100 | 2026-09-07 | Initial feature spec |
