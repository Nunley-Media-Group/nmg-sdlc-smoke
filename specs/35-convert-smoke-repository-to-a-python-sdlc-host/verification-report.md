# Verification Report: Convert smoke repository to a Python SDLC host

**Date**: 2026-08-31
**Issue**: #35
**Reviewer**: Codex (inline architecture and acceptance review)
**Scope**: Implementation verification against the approved issue #35 spec

---

## Executive Summary

The repository rewrite satisfies every local obligation in the approved issue #35 contract. The deterministic steering runner passed with complete zero-declaration coverage; the isolated editable install built version 3.14.0; 19 pytest tests, all 7 pytest-bdd scenarios, Ruff, installed-console success and rejection smoke checks, and the required deleted-workflow exercise all passed. The only remaining evidence is bounded to pull-request execution: the Python CI and managed contribution-gate checks must succeed for the exact PR head.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 5 |
| Architecture (SOLID) | 5 |
| Security | 5 |
| Performance | 5 |
| Testability | 5 |
| Error Handling | 5 |
| **Overall** | **5.0** |

### Implementation Status: PR Evidence Pending

**Architecture average**: 5.0/5.0  
**Local implementation issues**: 0

---

## Deterministic Steering Artifact and Ceiling

- Artifact: `.omp/sdlc/verification/35.json`
- Head identity: `c057af3afabb147c942417bfab473e6713748ccc`
- Spec hash: `sha256:e8331f10b9d7091c603b1e86baa445b903edf07e11f2939b57840aed56aed216`
- Steering hash: `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`
- Runner result: exit 0, `ok: true`
- Ceiling: none (`null`)
- Coverage: declared `0`, recorded `0`, complete `true`; missing, duplicate, and unknown lists are empty

The runner used issue 35, the exact spec directory, base `main`, and controller run id `5f0306e7-813a-4c9a-9247-7fce643926f9`. The validated manifest declares no project-specific deterministic validations, so zero declared and zero recorded results is complete coverage rather than missing evidence.

---

## Issue Scope

- Active issue: #35
- Spec: `specs/35-convert-smoke-repository-to-a-python-sdlc-host`
- Manifest: `implicit single issue`
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6, AC7]; FR [FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR11]; tasks [T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006, SCN007]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":35,"specPath":"specs/35-convert-smoke-repository-to-a-python-sdlc-host","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6","AC7"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5","FR6","FR7","FR8","FR9","FR10","FR11"],"tasks":["T001","T002","T003","T004","T005","T006","T007","T008","T009","T010","T011"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006","SCN007"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->
<!-- nmg-sdlc-pr-readiness: {"schemaVersion":1,"state":"pr_evidence_pending","issueNumber":35,"specPath":"specs/35-convert-smoke-repository-to-a-python-sdlc-host","local":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6","AC7"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5","FR6","FR7","FR8","FR9","FR10","FR11"],"tasks":["T001","T002","T003","T004","T005","T006","T007","T008","T009","T010","T011"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006","SCN007"],"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]},"tests":"pass","steeringGates":"pass"},"pendingEvidence":[{"kind":"required_check","name":"Python CI / verify","event":"pull_request","acceptanceCriteria":["AC5"]},{"kind":"required_check","name":"nmg-sdlc contribution gate / Validate nmg-sdlc contribution evidence","event":"pull_request","acceptanceCriteria":["AC6"]}]} -->

## Delivery Validation

- Local verification: **Pass**
- PR evidence: **Pending** — exact `pull_request` check results for `Python CI / verify` and `nmg-sdlc contribution gate / Validate nmg-sdlc contribution evidence`

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | Installable greeting happy path | Pass | Editable install built `nmg-sdlc-smoke-python==3.14.0`; `pyproject.toml:5-24`; `src/nmg_sdlc_smoke/greet.py:1-5`; full pytest passed. |
| AC2 | Console script happy path | Pass | `pyproject.toml:17-18`; `src/nmg_sdlc_smoke/cli.py:6-17`; installed `nmg-smoke Ada` exited 0 and printed exactly `Hello, Ada\n`. |
| AC3 | Blank name is rejected | Pass | `src/nmg_sdlc_smoke/greet.py:3-4`; `src/nmg_sdlc_smoke/cli.py:11-14`; installed CLI with whitespace exited 1, emitted no greeting, and printed the stable validation error on stderr. |
| AC4 | Independent Python verification | Pass | Isolated environment: 19 pytest tests passed, 7 feature scenarios passed, and Ruff reported `All checks passed!`; tests use repository-relative `pathlib` paths. |
| AC5 | Python CI replaces plugin verification | PR Evidence Pending | `.github/workflows/python-ci.yml:3-23` defines PR and main-push triggers, Python 3.12, editable dev install, pytest, feature pytest, and Ruff. The three named Node workflows are absent. Exact PR-event execution remains pending. |
| AC6 | Clean cutover preserves SDLC delivery contracts | Pass | Diff records deletion of copied plugin/runtime paths and live markers; only the #35 spec remains. `LICENSE` and `CHANGELOG.md` are unchanged from `main`; `VERSION` is 3.14.0 and dynamically read by `pyproject.toml`; the version-7 contribution gate, issue form, and AGENTS markers remain. |
| AC7 | Python-focused guidance | Pass | `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `steering/manifest.json`, and registered snippets describe the Python 3.12+ src-layout host, pytest, pytest-bdd, Ruff, and dynamic VERSION metadata rather than a current OMP plugin. |

---

## Regression Obligations

No separate regression AC, FR, or scenario IDs are declared. Preserved delivery contracts are evaluated under AC6 and T008-T010 and do not substitute for delivery completion.

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add packaging and VERSION 3.14.0 | Complete | Package metadata, exact seven-byte version file, and Python ignore rules are present. |
| T002 | Create import package skeleton | Complete | `src/nmg_sdlc_smoke/__init__.py` exports `greet`. |
| T003 | Implement greet | Complete | Exact happy path and `ValueError` contract implemented and tested. |
| T004 | Implement nmg-smoke CLI | Complete | Installed success and whitespace-failure paths observed. |
| T005 | Unit tests | Complete | `tests/test_greet.py` and `tests/test_cli.py`; full suite passed. |
| T006 | pytest-bdd feature and steps | Complete | SCN001-SCN007 exist with implemented independent steps; all 7 passed. |
| T007 | Python CI and Ruff; remove Node workflows | Complete locally | Workflow configuration and deletion state verified; Ruff passed. Hosted check remains PR-only evidence. |
| T008 | Remove copied plugin runtime | Complete | Required plugin/runtime paths are deleted; preserved files remain. |
| T009 | Rewrite docs and steering | Complete | Current guidance and the registered manifest runtime describe the Python host; legacy steering markdown is absent. |
| T010 | Rewrite rewrite-contract artifacts and managed gate | Complete | Rewrite artifacts name Python verification; contribution gate remains evaluator version 7 with the required manifest/module predicates and host comment. |
| T011 | Implementation PR evidence | PR Evidence Pending | Required changed paths are present in the diff. Exact PR title/body/head and hosted checks are controller delivery evidence. |

---

## Architecture Assessment

### Architecture Scores

| Area | Score (1-5) | Findings |
|------|-------------|----------|
| SOLID Principles | 5 | Proportional design: greeting policy is pure and isolated; CLI parsing and presentation stay in the adapter; no needless interface or service layer. |
| Security | 5 | External input is validated; no shell, network, database, secrets, dynamic execution, or runtime dependency surface exists. |
| Performance | 5 | One bounded validation pass and one interpolation; no avoidable collections, external calls, loops, or retained resources. |
| Testability | 5 | Pure business function, injectable argv, no mutable global state/network/time dependence, focused unit tests, and independent BDD scenarios. |
| Error Handling | 5 | One precise validation error is translated once at the CLI boundary to exit 1/stderr with no success output. |

### SOLID Compliance

| Principle | Score | Notes |
|-----------|-------|-------|
| Single Responsibility | 5 | `greet.py` owns validation/business output; `cli.py` owns process adaptation. |
| Open/Closed | 5 | The deliberately fixed one-command host needs no extension mechanism. |
| Liskov Substitution | 5 | No subtype hierarchy exists; no substitution contract is violated. |
| Interface Segregation | 5 | Public surface is one focused function and one CLI adapter. |
| Dependency Inversion | 5 | Business logic has no infrastructure dependency; argparse is confined to the adapter. |

### Layer Separation and Dependency Flow

`nmg_sdlc_smoke.cli` depends inward on `nmg_sdlc_smoke.greet`; the pure greeting module does not depend on CLI, tests, CI, or repository layout. Runtime dependencies remain zero. LSP diagnostics reported no issues in `src/**/*.py`.

### Security Findings

Authentication, authorization, transport, persistence, browser, and rate-limiting checks are not applicable. Relevant checks pass: input is validated at the business boundary, never sent to a shell, and rejected with a stable non-sensitive message.

### Performance Findings

Caching, async, database, pagination, networking, and graceful shutdown are not applicable. Runtime work is bounded by supplied name length and holds no resources.

### Testability Findings

Observable runtime contracts have unit and BDD coverage. Scenario setup is deterministic and repository-relative. Installed console-script smoke provides packaging-to-process evidence beyond direct `main()` tests.

### Error-Handling Findings

No error is swallowed. The domain function raises the approved `ValueError`; the CLI catches that error only and converts it to the approved exit status and stderr behavior. A custom hierarchy would add weight without improving this contract.

---

## Test Results

| Command / scenario | Result | Evidence |
|--------------------|--------|----------|
| `python3 -m venv .venv` and `.venv/bin/python -m pip install -e ".[dev]"` | Pass | Editable package built and installed as version 3.14.0 in an isolated environment. |
| Mandatory deterministic steering runner | Pass | Exit 0; `ok: true`; no ceiling; coverage declared 0, recorded 0, complete true. |
| `.venv/bin/python -m pytest` | Pass | 19 passed; 13 third-party Gherkin deprecation warnings; 0 failures. |
| `.venv/bin/python -m pytest tests/features` | Pass | 7 passed; SCN001-SCN007; 0 failures. |
| `.venv/bin/python -m ruff check .` | Pass | `All checks passed!` |
| Installed `.venv/bin/nmg-smoke Ada` | Pass | Exit 0; stdout `Hello, Ada\n`. |
| Installed `.venv/bin/nmg-smoke '   '` | Pass | Exit 1; no stdout greeting; stderr `nmg-smoke: error: name must not be blank\n`. |
| `git diff --quiet main -- LICENSE CHANGELOG.md` | Pass | Exit 0; preserved release files are unchanged. |

### BDD Coverage

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 / SCN001 | Yes | Yes | Yes |
| AC2 / SCN002 | Yes | Yes | Yes |
| AC3 / SCN003 | Yes | Yes | Yes |
| AC4 / SCN004 | Yes | Yes | Yes |
| AC5 / SCN005 | Yes | Yes | Locally; PR check pending |
| AC6 / SCN006 | Yes | Yes | Yes |
| AC7 / SCN007 | Yes | Yes | Yes |

- Feature files: 1
- BDD scenarios: 7/7 implemented and locally passing
- Unit plus BDD tests: 19 passing
- Step definitions: implemented

---

## Exercise Test Results

Plugin workflow changes were detected because the approved cutover deletes `workflows/`, `agents/`, and `commands/`. The first changed workflow, `address-pr-comments`, was exercised from a disposable Git repository with:

`node "/Volumes/Fast Brick/source/repos/nmg-sdlc/scripts/exercise-omp.mjs" --cwd <disposable-project> -- /sdlc-address-pr-comments <dry-run constraint>`

The harness completed normally without a wall-clock deadline. It failed closed because no `NMG_SDLC_REMEDIATION` packet, issue argument, issue-number branch, controller run id, or session token existed. It selected no command, did not invoke `scripts/sdlc-deliver.mjs`, executed no `gh` mutation, and changed no project file. The disposable project was removed. This is the expected safe lifecycle behavior for the deleted plugin surface; the resulting Python host has no OMP extension to exercise.

---

## Fixes Applied

No implementation fix was required. The pre-existing report was regenerated against the revised approved spec and current deterministic artifact; this is report correction, not a product-code change.

---

## Remaining Issues

No local implementation, architecture, security, performance, testability, or error-handling issue remains.

| Severity | Category | Location | Issue | Reason Not Fixed |
|----------|----------|----------|-------|------------------|
| External evidence | Delivery | GitHub pull request | Exact-head `pull_request` results for `Python CI / verify` and `nmg-sdlc contribution gate / Validate nmg-sdlc contribution evidence`, plus the T011 PR title/body identity, do not yet exist. | These are controller-owned PR-only facts and are the bounded basis for `PR Evidence Pending`. |

---

## Positive Observations

- Package metadata, runtime behavior, tests, CI commands, docs, managed steering, and rewrite evidence agree on one Python 3.12+ contract.
- The clean dependency direction and zero runtime dependencies match the approved minimal design.
- The rewrite removes the copied plugin surface while preserving LICENSE, CHANGELOG history, the version-7 managed contribution gate, managed issue form, and AGENTS spec-context markers.

---

## Files Reviewed

| Area | Files / evidence | Issues |
|------|------------------|--------|
| Approved spec | `requirements.md`, `design.md`, `tasks.md`, `feature.gherkin` | 0 |
| Runtime/package | `pyproject.toml`, `VERSION`, `.gitignore`, `src/nmg_sdlc_smoke/*.py` | 0 |
| Tests | `tests/test_greet.py`, `tests/test_cli.py`, `tests/features/**` | 0 |
| CI/managed contracts | `.github/workflows/*.yml`, issue form, `AGENTS.md`, `CONTRIBUTING.md` | 0 local; PR checks pending |
| Steering | `steering/manifest.json`, modules, snippets, retrospective state | 0 |
| Rewrite evidence | `references/rewrite-contract.*`, `references/rewrite-verification.md`, changed-path diff | 0 |

---

## Recommendation

**Ready for controlled draft PR evidence collection.** Every local acceptance, architecture, test, smoke, exercise, and deterministic steering obligation passed. Delivery must now collect the two declared PR-event checks for the exact head and verify the controller-owned T011 PR contract.
