# Requirements: Add second serial lifecycle smoke marker

**Issue**: #12
**Date**: 2026-08-24
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** maintainer validating serial lifecycle delivery
**I want** a second deterministic repository marker
**So that** the second serial lifecycle item has an exact, documented, automatically verified completion signal

---

## Background

The serial lifecycle smoke flow needs an independent completion signal for its second item. The repository currently has no root `LIVE_SMOKE_B.txt`, and `README.md` does not document this marker. The enhancement is repository evidence rather than a lifecycle behavior change: a byte-stable root file, one public documentation sentence, and one Jest ESM contract test provide the complete signal.

The implementation follows the established repository-root and `scripts/__tests__/` conventions. Issue #12 remains independent of other marker issues: it does not create, modify, or depend on another smoke marker.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Add the exact root marker

**Given** the enhancement has been implemented
**When** root `LIVE_SMOKE_B.txt` is read as bytes
**Then** the file exists
**And** its complete byte sequence is the UTF-8 bytes for `smoke-b-213` followed by exactly one LF byte (`0x0A`), with no BOM or other bytes

### AC2: Document the marker

**Given** the same implemented checkout
**When** `README.md` is read
**Then** the documentation identifies root `LIVE_SMOKE_B.txt` as the second serial lifecycle marker
**And** it states that the complete content is `smoke-b-213` followed by exactly one final newline

### AC3: Verify the valid marker deterministically

**Given** `LIVE_SMOKE_B.txt` has the required exact bytes
**When** `npm test -- --runTestsByPath __tests__/live-smoke-b.test.mjs` runs from `scripts/`
**Then** the Jest process exits zero
**And** the test uses no network, clock, or environment-dependent input

### AC4: Detect marker drift

**Given** `LIVE_SMOKE_B.txt` is missing, has different text, has extra bytes, or has a missing or additional final newline
**When** the same focused Jest test runs
**Then** the Jest process exits non-zero because the complete file bytes do not equal `smoke-b-213\n`

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Create root `LIVE_SMOKE_B.txt` with the exact byte sequence represented by `smoke-b-213\n`. | Must | UTF-8 text, one final LF, no BOM, no leading or trailing spaces, and no additional newline. |
| FR2 | Add one sentence under README `## Verification Gates` that names `LIVE_SMOKE_B.txt`, names `smoke-b-213`, identifies it as the second serial lifecycle marker, and states the one-final-newline contract. | Must | Preserve all unrelated README content. |
| FR3 | Add `scripts/__tests__/live-smoke-b.test.mjs` using the repository's Jest ESM and `repoRoot` conventions, read the marker without a text encoding, and compare the returned `Buffer` with `Buffer.from('smoke-b-213\n', 'utf8')`. | Must | Missing files and every byte mismatch fail; canonical bytes pass without external inputs. |

---

## Out of Scope

- Changes to serial lifecycle execution behavior or workflow orchestration
- Creation or modification of any other smoke marker
- Dependency relationships with another issue
- README changes beyond the one marker sentence
- Performing the enhancement-to-minor version bump during implementation; delivery owns version synchronization

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #12 | 2026-08-24 | Initial feature spec |
