# Design: Add LIVE_SMOKE_259_A controller remediation marker

**Issue**: #23
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## Overview

Issue #23 adds one repository-root regular file whose entire contents are a fixed UTF-8 byte sequence. The file is a disposable acceptance marker for a live controller-remediation SDLC run. It is not an Oh My Pi command, workflow, agent, or runtime capability.

Implementation must not enter `src/`, workflow bundles, agents, extension registration, package configuration, GitHub Actions, `README.md`, or `scripts/__tests__/`. Existing root markers `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, and `LIVE_SMOKE_D.txt` stay byte-for-byte unchanged.

---

## File Contract

| Path | Change | Contract |
|------|--------|----------|
| `LIVE_SMOKE_259_A.txt` | Create | Entire file is the UTF-8 byte sequence for `controller remediation smoke A` followed by exactly one LF (`0x0A`). Equivalent Node check: `Buffer.from('controller remediation smoke A\n', 'utf8')`. |

No other tracked path is in scope. Do not add `scripts/__tests__/live-smoke-259-a.test.mjs` or any README sentence.

---

## API and Runtime Impact

There are no new endpoints, commands, configuration keys, schemas, state transitions, UI components, runtime dependencies, or production code paths. Completeness is the presence of the exact root-file bytes, not a new automated test.

---

## Testing Strategy

| Layer | Command or evidence | Required result |
|-------|---------------------|-----------------|
| Exact artifact | Read root `LIVE_SMOKE_259_A.txt` as bytes (no text encoding) | Equals `Buffer.from('controller remediation smoke A\n', 'utf8')`. |
| Repository regression | From `scripts/`, run `npm test` | Existing Jest ESM contract tests pass. No new test file is added. |
| Sibling markers | Compare `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt` | Unchanged relative to the pre-implementation tree. |
| Completeness | Missing file, different text, extra bytes, missing final LF, or extra newline | Issue #23 is not complete. No substitute path or token satisfies FR1. |
| BDD traceability | Compare `requirements.md` AC1–AC3 with `feature.gherkin` `@SCN001`–`@SCN003` | One stable scenario maps to each acceptance criterion. |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #23 | 2026-08-25 | Initial feature spec |
