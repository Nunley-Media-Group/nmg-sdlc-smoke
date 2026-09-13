# Requirements: Add nmg-smoke --quotes flag for nmg-sdlc #379 verification

**Issue**: #109
**Date**: 2026-09-13
**Status**: Approved
**Author**: NMG

## User Story

**As a** maintainer running the registered final verification for Nunley-Media-Group/nmg-sdlc#379
**I want** one tiny optional `--quotes` formatting flag in the disposable `nmg-smoke` CLI
**So that** the registered provider can exercise canonical spec publication and normal consumer delivery against one fresh fixture

## Background

This is the single verification fixture for Nunley-Media-Group/nmg-sdlc#379. It is not independent backlog work, and no second #379 fixture is authorized.

The current CLI supports `--uppercase`, `--repeat COUNT`, `--prefix TEXT`, `--no-newline`, `--parentheses`, `--braces`, and a required name. It has no `--quotes` flag. The new long-only boolean flag wraps the fully composed message in one literal double-quote character on each side after the existing uppercase, prefix, parentheses, and braces transformations and before repeat/newline output. Omitting the flag preserves current output byte-for-byte.

Exactly two Gherkin scenarios are authorized. Spec publication must not implement this issue, run `/sdlc-execute`, open a feature PR, or alter existing smoke issues, specs, or backlog.

## Acceptance Criteria

### AC1: Quotes wrap the fully composed greeting

**Given** the installed `nmg-smoke` console script and a valid name
**When** `nmg-smoke --quotes --uppercase --prefix 'ok: ' --parentheses --braces Ada` runs
**Then** it exits 0
**And** stdout is exactly `"{(ok: HELLO, ADA)}"` followed by one newline
**And** stderr is empty

### AC2: Omitting quotes preserves current output

**Given** the installed `nmg-smoke` console script and a valid name
**When** `nmg-smoke Ada` runs without `--quotes`
**Then** it exits 0
**And** stdout is exactly `Hello, Ada` followed by one newline
**And** stderr is empty

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Add a long-only boolean `--quotes` flag that wraps the fully composed message in literal `"` characters after existing formatting and before repeat/newline output. | Must | No short alias; no escaping or content rewriting. |
| FR2 | Omitting `--quotes` preserves existing output, validation, repeat, newline, and library behavior. | Must | Keep zero runtime dependencies. |
| FR3 | Cover AC1 and AC2 with exactly two observable BDD scenarios and focused CLI tests. | Must | No additional scenarios. |
| FR4 | Keep implementation scope to CLI source, focused unit/BDD tests, README, CHANGELOG, and delivery-owned VERSION. | Must | `pyproject.toml` continues reading VERSION dynamically. |

## Scope

In scope: `src/nmg_sdlc_smoke/cli.py`, focused `tests/test_cli.py` coverage, one feature file, one pytest-bdd step module, README, CHANGELOG, and the normal delivery-owned 3.x VERSION bump.

Out of scope: changes to `greet`, package exports, dependencies, existing option semantics, existing issues/specs/backlog, implementation during spec publication, `/sdlc-execute`, or a feature PR during provisioning.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #109 | 2026-09-13 | Initial feature spec for the single nmg-sdlc #379 verification fixture |
