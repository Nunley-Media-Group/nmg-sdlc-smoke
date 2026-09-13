# Requirements: Add nmg-smoke braces flag

**Issue**: #105
**Date**: 2026-09-08
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer using the Python smoke CLI
**I want** an optional outermost literal curly-brace wrapper around each fully formatted greeting
**So that** I can compose braces with existing formatting without changing default output.

## Background

A fresh minimal enhancement for mandatory nmg-sdlc #372 T004 registered validation. This is a distinct issue, not a replacement for #374 or a replay of closed smoke #102. Publication authorizes this spec only; implementation and execution belong to the final registered372 provider after current candidate/code readiness.

## Current State

The merged CLI applies uppercase to the greeting, prepends the literal prefix, optionally wraps the message in parentheses, then repeats it with existing newline handling. There is no braces flag.

## Acceptance Criteria

### AC1: Enabled braces compose outermost with existing flags

**Given** the smoke CLI is available
**When** `nmg-smoke --braces --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada` is run
**Then** exit status is 0, stderr is empty, and stdout is exactly `{(ok: HELLO, ADA)}\n{(ok: HELLO, ADA)}` (each \n denotes one LF; no final LF).

### AC2: Absent braces preserve composed and default output

**Given** the smoke CLI is available
**When** `nmg-smoke --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada` and `nmg-smoke Ada` are run without braces
**Then** both exit 0 with empty stderr, and stdout is respectively `(ok: HELLO, ADA)\n(ok: HELLO, ADA)` and `Hello, Ada\n` (each \n denotes one LF).

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | Add long-only boolean --braces, disabled when absent. | Must |
| FR2 | Add literal { and } around the fully formatted message after all existing formatting, including parentheses, and before repetition/newline output. | Must |
| FR3 | Preserve content literally, existing errors and library APIs, and byte-identical output when absent. | Must |

## Out of Scope

- New dependencies, library changes, other flags, or changes to stopped96/98/100 and closed102.
- Execution in the authoring clone, provider runs, queue writes, or new handoffs.
- Implementation-owned VERSION changes; release version selection remains delivery-owned on v3.

## Notes

Exactly two independent BDD scenarios. Current major milestone v3. No external issue dependencies.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #105 | 2026-09-08 | Initial feature spec |
