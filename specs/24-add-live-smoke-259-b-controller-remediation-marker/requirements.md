# Requirements: Add LIVE_SMOKE_259_B controller remediation marker

**Issue**: #24
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## User Story

**As a** controller-remediation smoke operator
**I want** a disposable root acceptance marker `LIVE_SMOKE_259_B.txt` whose bytes are fixed and known
**So that** a live SDLC run can prove a second isolated issue was specified, implemented, verified, and delivered without changing other product behavior

---

## Background

This repository needs a second isolated disposable acceptance marker for a fresh live smoke of controller remediation. The marker is evidence that the lifecycle completed; it is not an Oh My Pi command, workflow, agent, or runtime capability.

Existing root markers `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, and `LIVE_SMOKE_D.txt` stay unchanged and are not owners of this contract. GitHub issue #23 owns a separate marker contract and is not a parent, blocker, or dependency of this issue. This issue adds only `LIVE_SMOKE_259_B.txt`. Do not treat nmg-sdlc plugin issue 259 as a GitHub parent of this issue.

Root already contains independent lifecycle markers: `LIVE_SMOKE_A.txt` (`smoke-a-213` plus one LF), `LIVE_SMOKE_B.txt` (`smoke-b-213` plus one LF), `LIVE_SMOKE_C.txt` (`LIVE_SMOKE_C` plus one LF), and `LIVE_SMOKE_D.txt` (`LIVE_SMOKE_D` plus one LF). Those earlier marker issues also documented README sentences and Jest exact-byte tests. `LIVE_SMOKE_259_B.txt` does not exist. No source, spec, or test currently names `LIVE_SMOKE_259_B`. This issue is a greenfield root-file addition only and must not adopt the earlier README-plus-test pattern.

---

## Acceptance Criteria

Each criterion becomes a Gherkin scenario.

### AC1: Root marker has exact bytes

**Given** a repository checkout after this issue is implemented
**When** root `LIVE_SMOKE_259_B.txt` is read as bytes
**Then** the file exists
**And** its complete byte sequence is the UTF-8 bytes for `controller remediation smoke B` followed by exactly one LF byte (`0x0A`), with no BOM, no leading or trailing spaces, and no additional newline

### AC2: Existing verification stays green

**Given** the same implemented checkout
**When** the repository's existing verification suite runs
**Then** those existing checks still pass
**And** `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, workflows, agents, extension commands, and other product behavior are unchanged

### AC3: Missing or wrong bytes are incomplete

**Given** `LIVE_SMOKE_259_B.txt` is missing, has different text, has extra bytes, or has a missing or additional final newline
**When** the delivered change is checked against this issue
**Then** the issue is not complete
**And** no substitute path or token satisfies the contract

---

## Functional Requirements

| ID | Requirement | Priority | Notes |
|----|-------------|----------|-------|
| FR1 | Add repository-root `LIVE_SMOKE_259_B.txt` whose complete bytes are UTF-8 `controller remediation smoke B` plus exactly one LF (`0x0A`). | Must | No BOM, no leading or trailing spaces, no additional newline. |
| FR2 | Leave every other tracked product file and existing verification contract unchanged. | Must | Do not add README documentation or a new Jest/contract test. |
| FR3 | Deliver the change through the complete SDLC lifecycle for this issue until the marker exists with those exact bytes. | Must | Owned by `/sdlc-execute #24` after this spec is approved; this spec package does not create the marker. |

---

## Out of Scope

- Changing `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `LIVE_SMOKE_259_A.txt`, or any other existing marker
- Adding README documentation or a new Jest/contract test for this disposable marker
- Changing SDLC workflows, agents, extension commands, GitHub Actions, or plugin runtime behavior
- Creating additional issues or official blocked-by edges
- Depending on, blocking, or parenting GitHub issue #23

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #24 | 2026-08-25 | Initial feature spec |
