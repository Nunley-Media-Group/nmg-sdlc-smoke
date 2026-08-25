# Design: Add LIVE_SMOKE_214_C success-path marker

**Issue**: #31
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## Overview

Issue #31 adds one repository-root regular file whose entire contents are a fixed UTF-8 byte sequence. The file is a disposable acceptance marker for the LIVE_SMOKE_214_C success-path smoke. It is not an Oh My Pi command, workflow, agent, or runtime capability.

This spec package does not create the marker. Implementation under `/sdlc-execute #31` creates it. Until that implementation, root `LIVE_SMOKE_214_C.txt` must remain absent; that absence is the expected success-path precondition and is not a failure.

Implementation must not enter `src/`, workflow bundles, agents, extension registration, package configuration, GitHub Actions, `README.md`, or `scripts/__tests__/`. Existing root markers `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `LIVE_SMOKE_259_A.txt`, and `LIVE_SMOKE_259_B.txt` stay byte-for-byte unchanged.

---

## File Contract

| Path | Change | Contract |
|------|--------|----------|
| `LIVE_SMOKE_214_C.txt` | Create during implementation only | Entire file is the UTF-8 byte sequence for `LIVE_SMOKE_214_C` followed by exactly one LF (`0x0A`). Equivalent Node check: `Buffer.from('LIVE_SMOKE_214_C\n', 'utf8')`. |

No other tracked path is in scope. Do not add `scripts/__tests__/live-smoke-214-c.test.mjs` or any README sentence.

---

## API and Runtime Impact

There are no new endpoints, commands, configuration keys, schemas, state transitions, UI components, runtime dependencies, or production code paths. Completeness after implementation is the presence of the exact root-file bytes, not a new automated test. Completeness before implementation is the continued absence of that file.

---

## Testing Strategy

| Layer | Command or evidence | Required result |
|-------|---------------------|-----------------|
| Pre-implementation precondition | `test ! -f LIVE_SMOKE_214_C.txt` from repository root | Exit 0. Absence is the expected success-path precondition, not a failure. |
| Exact artifact after implementation | Read root `LIVE_SMOKE_214_C.txt` as bytes (no text encoding) | Equals `Buffer.from('LIVE_SMOKE_214_C\n', 'utf8')`. |
| Repository regression | From `scripts/`, run `npm test` | Existing Jest ESM contract tests pass. No new test file is added. |
| Sibling markers | Compare `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `LIVE_SMOKE_259_A.txt`, `LIVE_SMOKE_259_B.txt` | Unchanged relative to the pre-implementation tree. |
| Completeness after implementation | Missing file, different text, extra bytes, missing final LF, or extra newline | Issue #31 is not complete. No substitute path or token satisfies FR1. |
| BDD traceability | Compare `requirements.md` AC1–AC4 with `feature.gherkin` `@SCN001`–`@SCN004` | One stable scenario maps to each acceptance criterion. |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #31 | 2026-08-25 | Initial feature spec |
