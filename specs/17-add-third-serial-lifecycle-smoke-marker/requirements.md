# Requirements: Add third serial lifecycle smoke marker

**Issue**: #17
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** nmg-sdlc smoke operator
**I want** a third byte-stable serial lifecycle marker
**So that** serial delivery can be proven by a minimal, documented, automatically checked artifact

---

## Background

The serial lifecycle smoke flow already has two independent root markers. A third serial item needs its own completion signal so an end-to-end run can prove it created, documented, and verified a new known artifact. This is repository evidence, not a lifecycle behavior change.

Root `LIVE_SMOKE_A.txt` and `LIVE_SMOKE_B.txt` already exist with tokens `smoke-a-213` and `smoke-b-213`. Their Jest files assert marker bytes only. This issue adds `LIVE_SMOKE_C.txt` with token `LIVE_SMOKE_C` (not a `smoke-c-*` variant) and a contract test that also asserts the README mention. It does not create, modify, or depend on A, B, or any other marker.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Root marker has exact bytes

**Given** the enhancement has been implemented
**When** root `LIVE_SMOKE_C.txt` is read as bytes
**Then** the file exists
**And** its complete byte sequence is the UTF-8 bytes for `LIVE_SMOKE_C` followed by exactly one LF byte (`0x0A`), with no BOM or other bytes

### AC2: README links and describes the marker

**Given** the same implemented checkout
**When** `README.md` is read
**Then** it links to root `LIVE_SMOKE_C.txt`
**And** it describes that marker as the third serial lifecycle smoke marker whose content is exactly `LIVE_SMOKE_C` followed by one newline

### AC3: Deterministic check accepts the valid marker and README mention

**Given** `LIVE_SMOKE_C.txt` has the required exact bytes and `README.md` links and describes that marker
**When** `npm test -- --runTestsByPath __tests__/live-smoke-c.test.mjs` runs from `scripts/`
**Then** the Jest process exits zero
**And** the test verifies both the file bytes and the README mention
**And** it uses no network, clock, or environment-dependent input

### AC4: Deterministic check rejects missing file, wrong bytes, or missing README mention

**Given** `LIVE_SMOKE_C.txt` is missing or its bytes differ from `LIVE_SMOKE_C` plus one newline, or `README.md` does not mention that marker
**When** the same focused Jest test runs
**Then** the Jest process exits non-zero

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Create root `LIVE_SMOKE_C.txt` with the exact byte sequence represented by `LIVE_SMOKE_C\n`. | Must | UTF-8 text, one final LF, no BOM, no leading or trailing spaces, and no additional newline. Token is `LIVE_SMOKE_C`, not `smoke-c-*`. |
| FR2 | Add one sentence under README `## Verification Gates` that links `LIVE_SMOKE_C.txt`, identifies it as the third serial lifecycle smoke marker, and states the exact one-newline contract. | Must | Preserve all unrelated README content, including the existing A and B sentences. |
| FR3 | Add `scripts/__tests__/live-smoke-c.test.mjs` using the repository's Jest ESM and `repoRoot` conventions; assert exact marker bytes and that README contains the documentation sentence. | Must | Missing files, every byte mismatch, and a missing README mention fail; canonical bytes plus the sentence pass without external inputs. |

---

## Out of Scope

- Runtime behavior, workflow orchestration, or lifecycle execution changes
- Dependency relationships with other issues or markers
- Refactors
- Changes beyond `LIVE_SMOKE_C.txt`, `README.md`, and `scripts/__tests__/live-smoke-c.test.mjs`
- Creating or modifying `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, or their existing checks
- Performing the enhancement-to-minor version bump during implementation; delivery owns version synchronization

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #17 | 2026-08-25 | Initial feature spec |
