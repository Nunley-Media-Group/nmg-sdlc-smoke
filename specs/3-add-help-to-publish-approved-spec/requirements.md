# Requirements: Add --help to publish-approved-spec

**Issue**: #3
**Date**: 2026-08-20
**Status**: Approved
**Author**: write-spec

---

## User Story

**As a** developer running the approved-spec publish helper
**I want** `--help` to print the existing usage line and exit 0
**So that** I can see supported commands without an invalid-arguments failure

---

## Background

`scripts/publish-approved-spec.mjs` dispatches `prepare`, `commit-push`, `merge`, and `default-branch`. Any other first token, including `--help` and a missing first token, currently calls `fail('invalid_arguments', { detail: USAGE })`, which writes JSON to stdout and exits 1. Operators cannot inspect supported commands without a failure.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: --help prints usage and succeeds

**Given** the helper is invoked as `node scripts/publish-approved-spec.mjs --help`
**When** the process starts
**Then** stdout includes `Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...`
**And** the process exits 0

### AC3: other first arguments are unchanged

**Given** the helper is invoked with first argument `prepare`, `commit-push`, `merge`, `default-branch`, missing, or any other token that is not exactly `--help`
**When** the process starts
**Then** dispatch and failure behavior match today's implementation
**And** `-h` remains `invalid_arguments` (not a help alias)

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | When `process.argv` after the script path has first token exactly `--help`, write the existing usage string plus a trailing newline to stdout and return from `main` so the process exits 0. | Must | Extra tokens after `--help` are ignored; still print usage and exit 0. |
| FR2 | Extract the current usage string into a `USAGE` constant and reuse it for both `--help` stdout and `fail('invalid_arguments', { detail: USAGE })`. | Must | Do not change the usage characters. |
| FR3 | `prepare`, `commit-push`, `merge`, and `default-branch` keep the same first-token dispatch. | Must | |
| FR4 | Missing first token and any first token other than the four commands and `--help` still call `fail('invalid_arguments', { detail: USAGE })` (JSON on stdout, exit 1). | Must | Includes `-h` and `--HELP`. |
| FR5 | Nested tokens such as `prepare --help` are not help. They enter `prepare` and fail as they do today (`invalid_arguments`, detail `issue must be a positive integer`). | Must | Out of scope: nested subcommand `--help`. |

---

## Out of Scope

- `-h`
- Nested subcommand `--help`
- Changing usage text
- New JSON success envelope for `--help`

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #3 | 2026-08-20 | Initial feature spec |
