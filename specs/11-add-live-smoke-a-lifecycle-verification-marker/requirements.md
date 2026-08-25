# Requirements: Add LIVE_SMOKE_A lifecycle verification marker

**Issue**: #11
**Date**: 2026-08-24
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** lifecycle smoke operator
**I want** a root LIVE_SMOKE_A marker with documented exact content and a deterministic Node test of those bytes
**So that** an end-to-end SDLC run can prove it created and verified a known artifact

---

## Background

The repository needs a small, byte-stable artifact that a live end-to-end lifecycle exercise can observe after specification and delivery. The artifact is evidence for the delivery pipeline rather than an OMP plugin capability: no extension command, workflow, agent, or runtime behavior changes.

The existing root `EXECUTE_SMOKE.md` marker belongs to issue #9 and remains unchanged. Issue #11 adds the independent root `LIVE_SMOKE_A.txt` contract, documents it in the public README, and protects its exact bytes with the repository's Jest ESM contract-test pattern under `scripts/__tests__/`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Root marker has exact bytes

**Given** a repository checkout after issue #11 is implemented
**When** root `LIVE_SMOKE_A.txt` is read as bytes
**Then** the file exists
**And** its complete byte sequence is the UTF-8 bytes for `smoke-a-213` followed by exactly one LF byte (`0x0A`), with no BOM or other bytes

### AC2: README documents the marker

**Given** the same implemented checkout
**When** `README.md` is read
**Then** it documents the root `LIVE_SMOKE_A.txt` lifecycle marker
**And** it names the token `smoke-a-213`

### AC3: Node contract test rejects missing or wrong content

**Given** `LIVE_SMOKE_A.txt` is missing or its bytes differ from `smoke-a-213` plus one LF byte
**When** `npm test -- --runTestsByPath __tests__/live-smoke-a.test.mjs` runs from `scripts/`
**Then** the Jest process exits non-zero because the exact-byte marker test fails

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Create root `LIVE_SMOKE_A.txt` with the exact byte sequence represented by `smoke-a-213\n`. | Must | UTF-8 text, one final LF, no BOM, no leading/trailing spaces, and no additional newline. |
| FR2 | Add one sentence under README `## Verification Gates` that names `LIVE_SMOKE_A.txt`, names `smoke-a-213`, and states the one-final-newline contract. | Must | Preserve all unrelated README content. |
| FR3 | Add `scripts/__tests__/live-smoke-a.test.mjs` using the repository's Jest ESM and `repoRoot` conventions, read the marker without a text encoding, and compare the returned `Buffer` with `Buffer.from('smoke-a-213\n', 'utf8')`. | Must | A missing file throws and fails the test; every byte mismatch fails the Buffer equality assertion. |

---

## Out of Scope

- Changing `EXECUTE_SMOKE.md` or issue #9's marker contract
- Adding other live-smoke files or tokens
- Changing SDLC workflows, agents, extension commands, or GitHub Actions
- Rewriting README beyond the one marker sentence
- Performing the enhancement-to-minor version bump during implementation; delivery owns version synchronization

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #11 | 2026-08-24 | Initial feature spec |
