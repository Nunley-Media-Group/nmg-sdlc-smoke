# Requirements: Add LIVE_SMOKE_214_C success-path marker

**Issue**: #31
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** lifecycle smoke operator
**I want** a repository-root LIVE_SMOKE_214_C success-path marker whose bytes are fixed and known
**So that** a live SDLC run can prove this isolated issue was specified, implemented, verified, and delivered without treating pre-implementation absence as a failure

---

## Background

This repository needs one isolated disposable acceptance marker for the LIVE_SMOKE_214_C success-path smoke. The marker is evidence that the lifecycle completed; it is not an Oh My Pi command, workflow, agent, or runtime capability.

The need is a single enhancement with no dependencies. Pre-implementation absence of the marker is the expected success-path precondition and must never be treated as a failure.

Root already contains independent lifecycle markers: `LIVE_SMOKE_A.txt` (`smoke-a-213` plus one LF), `LIVE_SMOKE_B.txt` (`smoke-b-213` plus one LF), `LIVE_SMOKE_C.txt` (`LIVE_SMOKE_C` plus one LF), `LIVE_SMOKE_D.txt` (`LIVE_SMOKE_D` plus one LF), `LIVE_SMOKE_259_A.txt` (`controller remediation smoke A` plus one LF), and `LIVE_SMOKE_259_B.txt` (`controller remediation smoke B` plus one LF). Earlier A–D marker issues also documented README sentences and Jest exact-byte tests; 259_A/259_B are greenfield root-file additions without README or new tests.

`LIVE_SMOKE_214_C.txt` does not exist. No source, spec, or test currently names `LIVE_SMOKE_214_C`. This issue is a greenfield root-file addition only and must not adopt the earlier README-plus-test pattern.

VERSION is `3.12.0` (major 3). Existing verification is `cd scripts && npm test`.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Root marker has exact bytes after implementation

**Given** a repository checkout after this issue is implemented
**When** root `LIVE_SMOKE_214_C.txt` is read as bytes
**Then** the file exists
**And** its complete byte sequence is the UTF-8 bytes for `LIVE_SMOKE_214_C` followed by exactly one LF byte (`0x0A`), with no BOM, no leading or trailing spaces, and no additional newline

### AC2: Pre-implementation absence is the expected success-path precondition

**Given** a repository checkout before this issue is implemented
**When** root `LIVE_SMOKE_214_C.txt` is inspected
**Then** the file is absent
**And** that absence is the expected success-path precondition
**And** the absence must not be treated as a failure, defect, or incomplete delivery of this issue

### AC3: Existing verification stays green

**Given** the same implemented checkout
**When** the repository's existing verification suite runs
**Then** those existing checks still pass
**And** existing markers, workflows, agents, extension commands, tests, README, and other product behavior are unchanged

### AC4: Missing or wrong bytes after implementation are incomplete

**Given** this issue is claimed complete but `LIVE_SMOKE_214_C.txt` is missing, has different text, has extra bytes, or has a missing or additional final newline
**When** the delivered change is checked against this issue
**Then** the issue is not complete
**And** no substitute path or token satisfies the contract

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Add repository-root `LIVE_SMOKE_214_C.txt` whose complete bytes are UTF-8 `LIVE_SMOKE_214_C` plus exactly one LF (`0x0A`). | Must | No BOM, no leading or trailing spaces, no additional newline. Create this file only during `/sdlc-execute #31` implementation, not during spec publication. |
| FR2 | Leave every other tracked product file and existing verification contract unchanged. | Must | Do not add README documentation or a new Jest/contract test. |
| FR3 | Treat pre-implementation absence of `LIVE_SMOKE_214_C.txt` as the expected success-path precondition, never as a failure. | Must | Absence before T001 is not a defect and does not make this issue incomplete. |

---

## Out of Scope

- Changing existing `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `LIVE_SMOKE_259_A.txt`, `LIVE_SMOKE_259_B.txt`, or any other existing marker
- Adding README documentation or a new Jest/contract test for this disposable marker
- Changing SDLC workflows, agents, extension commands, GitHub Actions, or plugin runtime behavior
- Creating additional issues or official blocked-by edges
- Treating pre-implementation absence as a bug or failed check

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #31 | 2026-08-25 | Initial feature spec |
