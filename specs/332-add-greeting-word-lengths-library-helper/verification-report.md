# Verification Report: Add greeting_word_lengths library helper

**Date**: 2026-11-20
**Issue**: #332
**Reviewer**: Claude (nmg-sdlc verify worker, gate phase)
**Scope**: Implementation verification against spec
**Verification head**: 4a4bd06733c8c07b73576965aa4da000024cd813

---

## Executive Summary

The branch adds the pure `greeting_word_lengths(name: str) -> list[int]` helper to `src/nmg_sdlc_smoke/greet.py`, exports it from `nmg_sdlc_smoke`, documents it in the README Library section, and implements the six `feature.gherkin` scenarios. The full review (at implementation head `00dbecde85da3bc199c47af928d5798d8d16e978`) passed with no finding above `info`. The gate head `4a4bd067` differs from the reviewed head only by the delivery preparation (`VERSION` 3.81.0 and a `CHANGELOG.md` entry). The registered pre-merge gate is complete and clean.

| Category | Score (1-5) |
|----------|-------------|
| Spec Compliance | 5 |
| Architecture (SOLID) | 5 |
| Security | 5 |
| Performance | 5 |
| Testability | 5 |
| Error Handling | 5 |
| **Overall** | 5.0 |

### Implementation Status: Pass
**Total Issues**: 0 (1 informational note)

---

## Issue Scope

- Active issue: #332
- Spec: `specs/332-add-greeting-word-lengths-library-helper`
- Manifest: implicit single issue
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6]; FR [FR1, FR2, FR3, FR4, FR5]; tasks [T001, T002]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":332,"specPath":"specs/332-add-greeting-word-lengths-library-helper","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5"],"tasks":["T001","T002"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Pass
- PR evidence: Not required

---

## Deterministic Steering Artifact and Ceiling

- Artifact: `.nmg-sdlc/verification/332.json`
- Identity: head `4a4bd06733c8c07b73576965aa4da000024cd813`, steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`, spec `sha256:51b3240029897841ae5560f44a9c9ec368c1c835cb1ccb7546e90c69ba2c665b`
- Base ref: `main`
- Ceiling: none
- Coverage: `declared: 0`, `recorded: 0`, `complete: true`, no missing, duplicate or unknown results
- Selection: `steering/manifest.json` declares no top-level `selection`, so no selection step ran
- Changed paths: `CHANGELOG.md`, `README.md`, `VERSION`, `src/nmg_sdlc_smoke/__init__.py`, `src/nmg_sdlc_smoke/greet.py`, `tests/features/add_greeting_word_lengths_library_helper.feature`, `tests/features/steps/test_greeting_word_lengths_steps.py`

The steering manifest registers no project validations (`validations: []`), so the gate is complete with zero declarations. No `repository.nmg-sdlc-smoke` or `project.nmg-sdlc-smoke` validation is declared, so the smoke requirement does not apply.

---

## Acceptance Criteria Verification

Evidence comes from the review record `.nmg-sdlc/verification/332-review.json` (full mode). Each criterion is exercised through the real public entry point. No criterion's tests mock the path under test.

| AC | Description | Status | Exercised | Evidence |
|----|-------------|--------|-----------|----------|
| AC1 | Return per-word lengths for simple and multi-word greetings | Pass | real entry point | `src/nmg_sdlc_smoke/greet.py:89-90`; SCN001 asserts `[[6,3],[6,3,8],[6,5,3]]` with exact `list`/`int` types |
| AC2 | Split on any whitespace without producing empty words | Pass | real entry point | `greeting_words` uses `str.split()`; SCN002 asserts tab, padded and double-space names, and no `0` length |
| AC3 | Count code points without normalization | Pass | real entry point | `len()` over `str`; SCN003 asserts `Zoë` (precomposed and combining) and emoji lengths |
| AC4 | Agree with the existing word helpers | Pass | real entry point | SCN004 compares against `greeting_words` and `greeting_word_count` with `zip(strict=True)` for six names |
| AC5 | Preserve invalid-name behavior | Pass | real entry point | SCN005 asserts `ValueError("name must not be blank")` for `""`, `" \t"`, `None`, `42` |
| AC6 | Expose and document the helper without changing existing surfaces | Pass | real entry point | `src/nmg_sdlc_smoke/__init__.py` export and `__all__`; README import, example and prose; SCN006 runs the README example in a subprocess and checks `cli.main(["Ada"])` |

### Functional Requirements

| FR | Status | Evidence |
|----|--------|----------|
| FR1 | Pass | `greet.py:89-90` matches design.md; pure, fresh list per call |
| FR2 | Pass | No exception handling in the helper; `greet` validation propagates unchanged |
| FR3 | Pass | Self-aliased import and `__all__` entry; no exports removed |
| FR4 | Pass | README Library section import, example and exact prose line |
| FR5 | Pass | `cli.py` and existing helpers unchanged; CLI output checked in SCN006 |

### Design Paths and Consumers

| Row | Status | Evidence |
|-----|--------|----------|
| DP1 (invalid names propagate `ValueError`) | Pass | SCN005 plus probes for bytes and U+3000-only names |
| DP2 (split yields no empty words) | Pass | SCN002 plus probes for U+3000 and U+001F separators |
| CON1 (package export) | Pass | `__init__.py` import and `__all__`, no duplicates |
| CON2 (README Library docs) | Pass | README example executes and prints `[6, 3]` |
| CON3 (acceptance feature collected by CI) | Pass | `tests/features/steps/test_greeting_word_lengths_steps.py` binds all six scenarios and is collected by `python -m pytest tests/features` |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Implement, export, and document greeting_word_lengths | Complete | `greet.py`, `__init__.py`, `README.md` |
| T002 | Implement the `feature.gherkin` scenarios | Complete | Feature file and step definitions for SCN001-SCN006 |

---

## Architecture Assessment

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 5 | One-line pure function built on `greeting_words` |
| Open/Closed | 5 | Additive only; no existing helper modified |
| Liskov Substitution | 5 | Not applicable beyond plain functions; no contract weakened |
| Interface Segregation | 5 | Minimal public addition to `__all__` |
| Dependency Inversion | 5 | Library does not depend on the CLI, tests or repository layout |

### Layer Separation

The helper lives in the pure library module. The CLI adapter is untouched.

### Dependency Flow

`greeting_word_lengths` -> `greeting_words` -> `greet`. No new imports or runtime dependencies.

---

## Security Assessment

- [x] Authentication: not applicable
- [x] Authorization: not applicable
- [x] Input validation: delegated to `greet`, which rejects non-string, blank and whitespace-only input
- [x] Injection prevention: no I/O, shell or evaluation
- [x] Data protection: no data persisted or transmitted

---

## Performance Assessment

- [x] Async patterns: not applicable
- [x] Caching: not needed; linear in greeting length
- [x] Resource management: no resources held
- [x] Query optimization: not applicable

---

## Test Coverage

### Scenario Coverage

| AC | Scenario | Implementation | Status |
|----|----------|----------------|--------|
| AC1 | `@SCN001` | `tests/features/steps/test_greeting_word_lengths_steps.py` | Implemented |
| AC2 | `@SCN002` | `tests/features/steps/test_greeting_word_lengths_steps.py` | Implemented |
| AC3 | `@SCN003` | `tests/features/steps/test_greeting_word_lengths_steps.py` | Implemented |
| AC4 | `@SCN004` | `tests/features/steps/test_greeting_word_lengths_steps.py` | Implemented |
| AC5 | `@SCN005` | `tests/features/steps/test_greeting_word_lengths_steps.py` | Implemented |
| AC6 | `@SCN006` | `tests/features/steps/test_greeting_word_lengths_steps.py` | Implemented |

### Test-Layer Findings

Kept test types: `bdd` (from `steering/test-layers.json`)

Among the test files the branch added or changed:

- Duplicate: none
- Non-kept type: none
- Justified: none

### Test Results

| Validation | Tier | Selection | Result |
|------------|------|-----------|--------|
| (none registered in `steering/manifest.json`) | n/a | n/a | Gate complete with `declared: 0` |

Supplementary local run at the gate head (not a registered validation), using the commands from the technology steering:

- `python -m pytest`: 1041 passed, 2 skipped
- `python -m pytest tests/features`: 351 passed, 2 skipped
- `python -m ruff check .`: All checks passed

---

## Fixes Applied

None. The review returned no repairable finding.

## Remaining Issues

### Critical Issues
None.

### High Priority
None.

### Medium Priority
None.

### Low Priority
None.

### Informational

| Field | Value |
|-------|-------|
| **Severity** | Info |
| **Category** | Testing |
| **Location** | `tests/features/steps/test_greeting_word_lengths_steps.py` |
| **Issue** | SCN006 checks the CLI through in-process `cli.main(["Ada"])` rather than the installed `nmg-smoke` console script |
| **Impact** | None; the console script maps to the same function (`pyproject.toml:18`) and tasks.md T002 specifies this check |
| **Reason Not Fixed** | No repair needed |

---

## Positive Observations

- The helper composes the existing word helper, so agreement with `greeting_words` and `greeting_word_count` holds by construction.
- Scenarios assert concrete values and exact types against the real public API, including Unicode edge cases and the README example run in a subprocess.

---

## Recommendations Summary

### Before PR (Must)
- None

### Short Term (Should)
- None

### Long Term (Could)
- Consider registering the steering test and lint commands as `builtin.command` validations so the gate records them.

---

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/greet.py` | 0 | New helper |
| `src/nmg_sdlc_smoke/__init__.py` | 0 | Export and `__all__` |
| `README.md` | 0 | Library documentation |
| `tests/features/add_greeting_word_lengths_library_helper.feature` | 0 | Six scenarios |
| `tests/features/steps/test_greeting_word_lengths_steps.py` | 0 | One info note |
| `VERSION` | 0 | 3.81.0 delivery preparation |
| `CHANGELOG.md` | 0 | Delivery preparation entry |

---

## Recommendation

**Ready for PR**

All six acceptance criteria and five functional requirements pass through the real entry point. The registered pre-merge gate is complete with no ceiling, and the supplementary test and lint run is green.
