# Requirements: Add --help to publish-approved-spec

**Issue**: #1
**Date**: 2026-08-20
**Status**: Approved
**Author**: Rich Nunley

---

## User Story

**As a** developer or maintainer running the approved-spec publisher
**I want** `scripts/publish-approved-spec.mjs` to accept `--help`
**So that** I can read the existing usage line without an invalid-arguments failure

---

## Background

The publisher is invoked as `node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...`. Usage is only surfaced today when the first argument is unrecognized, which is a failed run. Operators need a successful `--help` path that prints that same usage line on stdout and exits 0. This is a single tiny enhancement; subcommand behavior stays as it is.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: --help prints usage and succeeds

**Given** `scripts/publish-approved-spec.mjs` is run with Node
**When** the first argument is `--help`
**Then** stdout includes the existing usage line `Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...`
**And** the process exits 0
**And** stdout is not the invalid-arguments JSON object

### AC2: Known subcommands are unchanged

**Given** the first argument is `prepare`, `commit-push`, `merge`, or `default-branch`
**When** the script runs with the same remaining arguments as today
**Then** success and failure outcomes are unchanged

### AC3: Unrecognized first arguments still fail as today

**Given** the first argument is neither `--help` nor a known subcommand
**When** the script runs
**Then** stdout is still the invalid-arguments JSON object whose `detail` contains that same usage line
**And** the process exits 1

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | First argument `--help` prints the existing usage line on stdout and exits 0 | Must | First argv token only |
| FR2 | `prepare`, `commit-push`, `merge`, and `default-branch` keep their current behavior | Must | Including their current success and failure JSON |
| FR3 | Unrecognized first arguments keep the current invalid-arguments JSON stdout and exit 1 | Must | Includes `-h` |

---

## Out of Scope

- Short flag `-h`
- Changing the usage line text
- Help or usage for nested subcommand flags
- Changing JSON `ok` / `reasonCode` contracts for the four subcommands
- Other scripts

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #1 | 2026-08-20 | Initial feature spec |
