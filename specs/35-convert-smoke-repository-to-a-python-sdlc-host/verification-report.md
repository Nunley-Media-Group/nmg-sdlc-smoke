# Verification Report: Convert smoke repository to a Python SDLC host

**Date**: 2026-08-31
**Issue**: #35
**Reviewer**: Codex (inline architecture and acceptance review)
**Scope**: Implementation verification against the approved issue #35 spec

---

## Executive Summary

The Python cutover and managed steering remediation are locally complete: the deterministic steering runner passed with complete zero-declaration coverage, all 19 pytest tests passed, all 7 pytest-bdd scenarios passed, Ruff passed, and the installed `nmg-smoke` command produced the exact success and blank-input behavior. Hosted pull-request evidence for AC5/T011 remains a controller delivery-stage obligation.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 4 |
| Architecture (SOLID) | 5 |
| Security | 5 |
| Performance | 5 |
| Testability | 5 |
| Error Handling | 5 |
| **Overall** | **4.83** |

### Implementation Status: Locally Complete; PR Evidence Pending

**Architecture average**: 5.0/5.0  
**Total remaining issues**: 1

---

## Deterministic Steering Artifact and Coverage

- Artifact: `.omp/sdlc/verification/35.json`
- Head identity: `cb9f661da141f186b33e643daa52ea1cdebb2ca7`
- Spec hash: `sha256:6f002b69461d4fab76b235873f9efc1924651f1acdb6cea2021dd1de4b848a72`
- Steering hash: `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`
- Runner result: exit 0, `ok: true`
- Ceiling: none (`null`)
- Coverage: declared `0`, recorded `0`, complete `true`; missing, duplicate, and unknown lists are empty

The mandatory runner was invoked with issue 35, the exact spec directory, base `main`, and controller run id `5f0306e7-813a-4c9a-9247-7fce643926f9`. The approved managed manifest declares no deterministic validations, so zero declared and zero recorded results is complete coverage. The required pytest, pytest-bdd, and Ruff commands remain explicit local and CI checks rather than invented manifest registrations.

---

## Issue Scope

- Active issue: #35
- Spec: `specs/35-convert-smoke-repository-to-a-python-sdlc-host`
- Manifest: `implicit single issue`
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6, AC7]; FR [FR1, FR2, FR3, FR4, FR5, FR6, FR7, FR8, FR9, FR10, FR11]; tasks [T001, T002, T003, T004, T005, T006, T007, T008, T009, T010, T011]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006, SCN007]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":35,"specPath":"specs/35-convert-smoke-repository-to-a-python-sdlc-host","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6","AC7"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5","FR6","FR7","FR8","FR9","FR10","FR11"],"tasks":["T001","T002","T003","T004","T005","T006","T007","T008","T009","T010","T011"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006","SCN007"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: **Pass**
- PR evidence: **Pending** for AC5/T011; the deterministic steering gate and all local checks pass

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | Installable greeting happy path | Pass | Editable install built `nmg-sdlc-smoke-python==3.14.0`; `pyproject.toml:5-24`; `src/nmg_sdlc_smoke/greet.py:1-5`; isolated pytest run passed. |
| AC2 | Console script happy path | Pass | `pyproject.toml:17-18`; `src/nmg_sdlc_smoke/cli.py:6-17`; installed `/tmp/nmg-sdlc-smoke-35-verify/bin/nmg-smoke Ada` exited 0 with stdout exactly `Hello, Ada\n` and empty stderr. |
| AC3 | Blank name is rejected | Pass | `src/nmg_sdlc_smoke/greet.py:3-4`; `src/nmg_sdlc_smoke/cli.py:11-14`; installed CLI with whitespace exited 1, emitted no stdout, and emitted `nmg-smoke: error: name must not be blank\n` to stderr. |
| AC4 | Independent Python verification | Pass | Isolated Python environment: `python -m pytest` passed 19 tests; `python -m pytest tests/features` passed 7 scenarios; `python -m ruff check .` reported `All checks passed!`; tests use repository-relative `pathlib` paths. |
| AC5 | Python CI replaces plugin verification | Partial | `.github/workflows/python-ci.yml:3-23` has pull-request and main-push triggers, Python 3.12, editable dev install, pytest, feature pytest, and Ruff. The three named Node workflows are absent. Hosted GitHub Actions execution is PR-only and not yet evidenced. |
| AC6 | Clean cutover preserves SDLC delivery contracts | Pass | `git diff --name-status main` shows deletion of plugin runtime, Node workflows, copied specs, and live markers; only the #35 spec remains. `git diff --quiet main -- LICENSE CHANGELOG.md` passed. Managed gate, issue form, 3.x `VERSION`, and AGENTS markers remain. |
| AC7 | Python-focused guidance | Pass | `README.md`, `CONTRIBUTING.md`, `AGENTS.md`, `steering/manifest.json`, and the registered `steering/snippets/` describe Python 3.12+, src layout, pytest, pytest-bdd, Ruff, and dynamic VERSION metadata; plugin prose is historical rather than current-product guidance. |

---

## Regression Obligations

No separate regression AC, FR, or scenario IDs are declared for this singular clean-cutover spec. Preserved delivery contracts are evaluated under AC6/T008-T010 and do not substitute for current delivery completion.

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add packaging and VERSION 3.14.0 | Complete | `pyproject.toml`, `VERSION`, and `.gitignore` match the packaging contract; editable build resolved version 3.14.0. |
| T002 | Create import package skeleton | Complete | `src/nmg_sdlc_smoke/__init__.py` imports and exports `greet`. |
| T003 | Implement greet | Complete | Exact success value and exact `ValueError` contract implemented and tested. |
| T004 | Implement nmg-smoke CLI | Complete | Exact success and whitespace failure paths observed against the installed console script. |
| T005 | Unit tests | Complete | `tests/test_greet.py` and `tests/test_cli.py`; full suite passed. |
| T006 | pytest-bdd feature and steps | Complete | SCN001-SCN007 exist and all 7 passed. |
| T007 | Python CI and Ruff; remove Node workflows | Complete locally | Workflow configuration and deletion state verified; Ruff passed. Hosted execution remains AC5 PR evidence. |
| T008 | Remove copied plugin runtime | Complete | Required deleted-path inventory is present in the diff; preserved LICENSE and CHANGELOG are unchanged. |
| T009 | Rewrite docs and steering | Complete | Current-product prose and retrospective state match the issue contract; the approved managed runtime now registers product, technology, and structure snippets and preserves the retrospective files. |
| T010 | Rewrite rewrite-contract artifacts and managed gate | Complete | Rewrite artifacts name Python verification; managed gate version 7 checks the registered manifest and module paths while retaining the Python-host marker. |
| T011 | Implementation PR evidence | Incomplete | Exact PR title/body, changed-head synchronization, and hosted evidence are controller/delivery-stage obligations not available in this local worktree review. |

---

## Architecture Assessment

### Architecture Scores

| Area | Score (1-5) | Findings |
|------|-------------|----------|
| SOLID Principles | 5 | Proportional to this two-function project: greeting policy is pure and isolated; CLI parsing/error presentation stays in the adapter; no needless interface or DI layer. |
| Security | 5 | All input is validated before use; no shell, network, database, secrets, dynamic execution, or runtime dependency surface; errors expose no internals. |
| Performance | 5 | One argument parse, one `strip()` validation pass, and one interpolation; no avoidable collections, I/O loops, blocking external calls, or persistent resources. |
| Testability | 5 | Pure business function, injectable argv, pytest capture, no global mutable state/network/time dependence, independent BDD scenarios. |
| Error Handling | 5 | One precise validation error, caught at the CLI boundary and converted to exit 1/stderr with no success output; argparse retains its standard missing-argument failure. |

### SOLID Compliance

| Principle | Score | Notes |
|-----------|-------|-------|
| Single Responsibility | 5 | `greet.py` owns validation/business output; `cli.py` owns argument and process adaptation. |
| Open/Closed | 5 | No extension mechanism is warranted for a deliberately fixed one-command host; adding one would be needless abstraction. |
| Liskov Substitution | 5 | No subtype hierarchy exists; no substitution contract is violated. |
| Interface Segregation | 5 | Public surface is one focused function plus one CLI adapter. |
| Dependency Inversion | 5 | Business logic has no concrete infrastructure dependency; argparse is confined to the entry adapter. |

### Layer Separation and Dependency Flow

`nmg_sdlc_smoke.cli` depends inward on `nmg_sdlc_smoke.greet`; the pure greeting module does not depend on CLI/process concerns. Runtime dependencies remain zero. The direction matches the approved design without introducing an abstraction beside the established minimal pattern.

### Security Findings

Authentication, authorization, transport, persistence, browser, and rate-limiting checks are not applicable. Relevant checks pass: type/blank validation occurs at the business boundary, the input is never sent to a shell, and stderr contains only the stable validation message.

### Performance Findings

Caching, async, database, pagination, networking, and graceful shutdown are not applicable. The implementation performs bounded work proportional only to the supplied name length and holds no resources.

### Testability Findings

All observable runtime contracts have unit and BDD coverage. Scenario setup is local and repeatable. The installed console-script smoke adds end-to-end packaging evidence beyond direct `main()` tests.

### Error-Handling Findings

No error is swallowed. The domain function raises the exact approved error; the adapter translates it once. A custom exception hierarchy would add weight without improving this single validation contract.

---

## Test Results

| Command / scenario | Result | Evidence |
|--------------------|--------|----------|
| `python3 -m venv /tmp/nmg-sdlc-smoke-35-verify` and editable dev install | Pass | Editable wheel built and installed as `nmg-sdlc-smoke-python-3.14.0`. |
| `node "/Volumes/Fast Brick/source/repos/nmg-sdlc/scripts/sdlc-verify-steering.mjs" --project . --issue 35 --spec specs/35-convert-smoke-repository-to-a-python-sdlc-host --base main --controller-run-id 5f0306e7-813a-4c9a-9247-7fce643926f9` | Pass | Exit 0; `ok: true`; no ceiling; coverage declared `0`, recorded `0`, complete `true`. |
| `/tmp/nmg-sdlc-smoke-35-verify/bin/python -m pytest` | Pass | 19 passed; 13 third-party Gherkin deprecation warnings; 0 failures. |
| `/tmp/nmg-sdlc-smoke-35-verify/bin/python -m pytest tests/features` | Pass | 7 passed; SCN001-SCN007; 0 failures. |
| `/tmp/nmg-sdlc-smoke-35-verify/bin/python -m ruff check .` | Pass | `All checks passed!` |
| Installed `nmg-smoke Ada` | Pass | Exit 0; stdout `Hello, Ada\n`; stderr empty. |
| Installed `nmg-smoke '   '` | Pass | Exit 1; stdout empty; stderr exact stable validation message. |

The first ambient `python` and Homebrew `python3` attempts lacked pytest, and direct Homebrew installation was correctly blocked by PEP 668. Verification then used a disposable isolated virtual environment; those environment setup failures are not implementation failures.

### BDD Coverage

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 / SCN001 | Yes | Yes | Yes |
| AC2 / SCN002 | Yes | Yes | Yes |
| AC3 / SCN003 | Yes | Yes | Yes |
| AC4 / SCN004 | Yes | Yes | Yes |
| AC5 / SCN005 | Yes | Yes | Locally; hosted CI pending |
| AC6 / SCN006 | Yes | Yes | Yes |
| AC7 / SCN007 | Yes | Yes | Yes |

- Feature files: 1
- BDD scenarios: 7/7 implemented and locally passing
- Unit tests plus BDD tests: 19 passing
- Step definitions: implemented

---

## Exercise Test Results

Plugin changes were detected because the approved cutover deletes `workflows/`, `agents/`, `commands/`, and `src/extension.ts`. The first changed workflow, `address-pr-comments`, was exercised from disposable Git repository `/tmp/nmg-sdlc-exercise-35` with `node "/Volumes/Fast Brick/source/repos/nmg-sdlc/scripts/exercise-omp.mjs" --cwd /tmp/nmg-sdlc-exercise-35 -- /sdlc-address-pr-comments` plus the required dry-run constraint. The harness completed normally in 81.40 seconds and failed closed without executing GitHub commands or modifying files: `/sdlc-address-pr-comments` requires an `NMG_SDLC_REMEDIATION` packet from `sdlc-deliver.mjs`, while the disposable project intentionally had no packet, issue-number branch, controller run ID, session token, or GitHub remote. This is a complete state-based exercise outcome for the removed workflow surface, not evidence for the Python runtime ACs. The changed Python runtime was separately exercised through the installed `nmg-smoke` console script, including both success and validation-error lifecycles.

---

## Fixes Applied

- Applied the approved `/sdlc-steering` migration: added `steering/manifest.json`, four managed modules, and three registered project snippets; removed the superseded Markdown authorities while preserving retrospective state.
- Updated `CONTRIBUTING.md`, the AC7 pytest-bdd step, and managed contribution gate version 7 to consume the registered managed runtime instead of deleted legacy paths.
- Reran the deterministic runner and all local behavior checks; no runtime, test, lint, or CLI defects remain.

---

## Remaining Issues

| Severity | Category | Location | Issue | Reason Not Fixed |
|----------|----------|----------|-------|------------------|
| Medium | Delivery / PR evidence | GitHub implementation PR | AC5 hosted Python 3.12 CI and T011 exact PR title/body/head evidence are not yet available. | Controller/delivery-stage evidence; cannot be established by local verification alone. |

---

## Positive Observations

- The runtime is three small modules with no runtime dependencies and no unnecessary abstraction.
- The package metadata, installed CLI, unit tests, BDD tests, Ruff configuration, CI commands, docs, and rewrite evidence agree on one Python 3.12+ contract.
- The repository rewrite removes the copied plugin surface while preserving the managed contribution gate, issue form, LICENSE, CHANGELOG history, and AGENTS spec-context markers.
- Managed contribution-gate version 7 checks the registered manifest and module paths; the Python-host marker remains.

---

## Files Reviewed

| Area | Files / evidence | Issues |
|------|------------------|--------|
| Approved spec | `requirements.md`, `design.md`, `tasks.md`, `feature.gherkin` | 0 |
| Runtime/package | `pyproject.toml`, `VERSION`, `.gitignore`, `src/nmg_sdlc_smoke/*.py` | 0 |
| Tests | `tests/test_greet.py`, `tests/test_cli.py`, `tests/features/**` | 0 |
| CI/managed contracts | `.github/workflows/*.yml`, `.github/ISSUE_TEMPLATE/nmg-sdlc-ready-issue.yml`, `AGENTS.md`, `CONTRIBUTING.md` | 0 implementation defects |
| Product guidance | `README.md`, `steering/manifest.json`, `steering/modules/`, `steering/snippets/`, `steering/retrospective-state.json` | 0 |
| Rewrite evidence | `references/rewrite-contract.json`, `references/rewrite-contract.md`, `references/rewrite-verification.md`, full `git diff --name-status main` | 0 |

---

## Recommendation

**Ready for controller verification and delivery.** The managed steering runtime is valid, the deterministic artifact has complete coverage with no ceiling, and all local commands pass. The controller must still establish exact-head hosted Python 3.12 CI and T011 pull-request evidence.
