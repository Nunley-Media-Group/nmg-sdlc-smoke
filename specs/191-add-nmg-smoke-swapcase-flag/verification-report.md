# Verification Report: Add nmg-smoke --swapcase flag

**Date**: 2026-09-30
**Issue**: #191
**Reviewer**: Codex
**Scope**: Implementation verification against spec

**Verification head**: d533a4ea9915a85ae7cc3f765d5f6e4c80581132

---

## Executive Summary

The branch `191-add-nmg-smoke-swapcase-flag` contains no implementation. Local HEAD, `origin/191-add-nmg-smoke-swapcase-flag`, and `main` all resolve to `d533a4ea9915a85ae7cc3f765d5f6e4c80581132` (`docs: approve spec for #191 (#192)`). `git diff main...HEAD` is empty. `src/nmg_sdlc_smoke/cli.py` does not register `--swapcase`, and running the installed console script with it exits 2 with `unrecognized arguments: --swapcase`. None of the four tasks (T001–T004) have been done, and all six delivery acceptance criteria fail. The regression obligations still hold because baseline behavior is unchanged.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 1 |
| Architecture (SOLID) | 4 |
| Security | 5 |
| Performance | 5 |
| Testability | 2 |
| Error Handling | 4 |
| **Overall** | 3.5 |

Architecture, security, performance and error-handling scores apply to the unchanged baseline CLI only. This branch has no delta to review.

### Implementation Status: Fail
**Total Issues**: 4

---

## Deterministic Steering Artifact and Ceiling

- Runner: `sdlc-verify-steering.mjs --project . --issue 191 --spec specs/191-add-nmg-smoke-swapcase-flag --base main --controller-run-id b80da6ff-53ea-4367-8832-20a2c38ea7d1`
- Artifact: `.omp/sdlc/verification/191.json`
- Identity: head `d533a4ea9915a85ae7cc3f765d5f6e4c80581132`, steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`, spec `sha256:7d1c27662c00d7401faac7b7b381f603c7716b2e72c9db1a733b449ce11c362b`
- Ceiling: `null`
- Coverage: declared 0, recorded 0, complete `true`. `steering/manifest.json` registers no project validations, so `repository.nmg-sdlc-smoke` is not declared and no real smoke lifecycle evidence is required.
- Changed paths vs `main`: none

---

## Issue Scope

- Active issue: #191
- Spec: `specs/191-add-nmg-smoke-swapcase-flag`
- Manifest: implicit single issue
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6]; FR [FR1, FR2, FR3, FR4, FR5]; tasks [T001, T002, T003, T004]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":191,"specPath":"specs/191-add-nmg-smoke-swapcase-flag","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5"],"tasks":["T001","T002","T003","T004"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Not complete
- PR evidence: Not required

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `nmg-smoke --swapcase Ada` → `hELLO, aDA\n`, exit 0 | Fail | Installed script: `nmg-smoke: error: unrecognized arguments: --swapcase`, exit 2; `src/nmg_sdlc_smoke/cli.py` `case` group has only `--uppercase`/`--lowercase` |
| AC2 | Composes with prefix/parentheses/repeat/no-newline | Fail | Flag unrecognized; there is no swapcase branch in `main()` |
| AC3 | `str.swapcase` semantics for `ÅSA` / `Straße` | Fail | Flag unrecognized |
| AC4 | `--swapcase` mutually exclusive with `--uppercase`/`--lowercase` → exit 2, `not allowed with argument` | Fail | Exit 2 comes from `unrecognized arguments`, not the mutual-exclusion error. `--swapcase` is not in the `case` group. |
| AC5 | `nmg-smoke --swapcase " "` → exit 1, blank-name error | Fail | Exits 2 with `unrecognized arguments: --swapcase` before name validation |
| AC6 | Default/uppercase/lowercase output preserved; `--help` lists `--swapcase` | Fail | `Hello, Ada`, `HELLO, ADA`, `hello, ada` are preserved, but the usage/help output `[-h] [--uppercase \| --lowercase] ...` does not list `--swapcase` |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add mutually exclusive `--swapcase` flag in `src/nmg_sdlc_smoke/cli.py` | Incomplete | No change in `cli.py` |
| T002 | Focused CLI unit tests in `tests/test_cli.py` | Incomplete | `tests/test_cli.py` has 0 `swapcase` references |
| T003 | `tests/features/add_nmg_smoke_swapcase_flag.feature` + `tests/features/steps/test_swapcase_steps.py` | Incomplete | Neither file exists |
| T004 | Document `--swapcase` in README `## CLI` | Incomplete | `README.md` has 0 `swapcase` references |

---

## Architecture Assessment

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 4 | `greet.py` stays pure, and `cli.py` handles parsing and rendering (baseline) |
| Open/Closed | 4 | Case flags are added through an argparse mutually exclusive group plus an `if/elif` chain. The design adds `--swapcase` as one more `elif`. |
| Liskov Substitution | 4 | Not applicable. There is no inheritance. |
| Interface Segregation | 4 | Minimal public API |
| Dependency Inversion | 4 | The CLI depends on the library, and the library has no dependency on the CLI |

### Layer Separation

The baseline is compliant: the library does not import the CLI. This branch introduces no change.

### Dependency Flow

`cli.py` → `greet.py` only. There are no runtime dependencies.

---

## Security Assessment

- [x] Authentication: N/A (local CLI)
- [x] Authorization: N/A
- [x] Input validation: blank names are rejected by `greet`, and argparse validates flags
- [x] Injection prevention: no shell, eval, or file I/O
- [x] Data protection: N/A

## Performance Assessment

- [x] Async patterns: N/A
- [x] Caching: N/A
- [x] Resource management: no resources are held
- [x] Query optimization: N/A

---

## Test Coverage

### BDD Scenarios

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 | No | No | No |
| AC2 | No | No | No |
| AC3 | No | No | No |
| AC4 | No | No | No |
| AC5 | No | No | No |
| AC6 | No | No | No |

### Test Execution (isolated venv, `python -m pip install -e ".[dev]"`, Python 3.14.7)

- `python -m pytest`: 427 passed, 2 skipped
- `python -m pytest tests/features`: 159 passed, 2 skipped
- `python -m ruff check .`: All checks passed

The suite passes only because no #191 tests exist. It provides no delivery evidence for #191.

---

## Fixes Applied

| Severity | Category | Location | Original Issue | Fix Applied | Routing |
|----------|----------|----------|----------------|-------------|---------|
| — | — | — | None | None. The verify publication scope allows only `verification-report.md`, and the missing implementation is a full implement-step deliverable rather than a safe local fix. | — |

## Remaining Issues

### Critical Issues

| Field | Value |
|-------|-------|
| **Severity** | Critical |
| **Category** | Architecture |
| **Location** | `src/nmg_sdlc_smoke/cli.py` |
| **Issue** | `--swapcase` is not registered in the `case` group and has no `message.swapcase()` branch (T001; AC1–AC6; FR1–FR3) |
| **Impact** | Every delivery acceptance criterion fails |
| **Reason Not Fixed** | Implementation is missing. The verify scope permits only the report, so this routes back to the implement step. |

### High Priority

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Category** | Testing |
| **Location** | `tests/test_cli.py`, `tests/features/add_nmg_smoke_swapcase_flag.feature`, `tests/features/steps/test_swapcase_steps.py` |
| **Issue** | The unit tests (T002) and the pytest-bdd scenarios SCN001–SCN006 (T003) are missing |
| **Impact** | No acceptance criterion has executable coverage |
| **Reason Not Fixed** | Outside the verify publication scope. This is implement-step work. |

| Field | Value |
|-------|-------|
| **Severity** | High |
| **Category** | Documentation |
| **Location** | `README.md` |
| **Issue** | The `--swapcase` documentation is missing (T004, FR5) |
| **Impact** | The user-facing behavior is undocumented |
| **Reason Not Fixed** | Outside the verify publication scope |

### Medium Priority

| Field | Value |
|-------|-------|
| **Severity** | Medium |
| **Category** | Process |
| **Location** | branch `191-add-nmg-smoke-swapcase-flag` |
| **Issue** | Verification was invoked on a branch whose HEAD equals `main` (spec-approval commit only) |
| **Impact** | Verification cannot pass until implementation commits exist |
| **Reason Not Fixed** | The controller has to route this back to implementation |

### Low Priority

None.

---

## Positive Observations

- The approved spec package is internally consistent. All four files declare `**Issue**: #191` and `**Status**: Approved`.
- The baseline CLI design (mutually exclusive `case` group, `if/elif` transform) makes the specified change a small, single-branch addition.
- Existing behavior (FR4) is preserved: `Hello, Ada`, `HELLO, ADA`, `hello, ada`.

---

## Recommendations Summary

### Before PR (Must)
- [ ] T001: add `case.add_argument("--swapcase", action="store_true")` after `--lowercase`, plus `elif args.swapcase: message = message.swapcase()`
- [ ] T002: add CLI unit tests for AC1–AC6
- [ ] T003: add the pytest-bdd feature and steps for SCN001–SCN006
- [ ] T004: add the README `## CLI` documentation for `--swapcase`

### Short Term (Should)
- [ ] Re-run full verification at the new implementation head

### Long Term (Could)
- None

---

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/cli.py` | 1 | `--swapcase` is absent |
| `tests/test_cli.py` | 1 | No `--swapcase` tests |
| `tests/features/` | 1 | No #191 feature or steps |
| `README.md` | 1 | No `--swapcase` docs |
| `steering/manifest.json` | 0 | Valid; no registered validations |

---

## Recommendation

**Major rework needed**

The implementation for #191 is completely absent at `d533a4ea9915a85ae7cc3f765d5f6e4c80581132`. The status is Fail, and the work routes back to implementation diagnosis. After T001–T004 are committed, the full registered gate has to be re-run.
