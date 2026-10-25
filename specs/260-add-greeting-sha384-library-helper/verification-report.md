# Verification Report: Add greeting_sha384 library helper

**Date**: 2026-10-25
**Issue**: #260
**Reviewer**: Claude (nmg-sdlc verify worker)
**Scope**: Implementation verification against spec
**Verification head**: 3e112065d688be81a4f064d052f921b1b7d6d332

---

## Executive Summary

`greeting_sha384` is implemented as a one-line pure helper that matches the design exactly. It is exported from the package root, documented in the README Library section, and covered by 9 unit tests and 4 pytest-bdd scenarios. All required local checks pass: pytest, pytest-bdd, and Ruff. The deterministic steering gate is complete and declares no project validations. No findings required fixes.

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
**Total Issues**: 0

---

## Issue Scope

- Active issue: #260
- Spec: `specs/260-add-greeting-sha384-library-helper`
- Manifest: implicit single issue
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4]; FR [FR1, FR2, FR3, FR4, FR5]; tasks [T001, T002, T003]; scenarios [SCN001, SCN002, SCN003, SCN004]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":260,"specPath":"specs/260-add-greeting-sha384-library-helper","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5"],"tasks":["T001","T002","T003"],"scenarios":["SCN001","SCN002","SCN003","SCN004"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Pass
- PR evidence: Not required

---

## Deterministic Steering Artifact

- Runner: `sdlc-verify-steering.mjs --base main --controller-run-id c68366d8-f041-496d-bbd0-767c4cf485e2`. It exited 0 with `ok: true` and `ceiling: null`.
- Artifact: `.nmg-sdlc/verification/260.json`
  - head `3e112065d688be81a4f064d052f921b1b7d6d332`
  - steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`
  - spec `sha256:a1721ef700af2f03dad5609b58f4c162bee9597182e5d5002e659d8d21a8ba27`
- Coverage: `declared: 0`, `recorded: 0`, `complete: true`. The manifest declares no project-specific validations, so this is a complete gate with no ceiling. `steering/manifest.json` has `validations: []` and `extensions: []`, so no `repository.nmg-sdlc-smoke` or `project.nmg-sdlc-smoke` provider is declared and no real smoke lifecycle result is required.

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | SHA-384 hex digest of completed greeting for `Ada` and `Ada Lovelace` | Pass | `src/nmg_sdlc_smoke/greet.py:103-104`. `test_greeting_sha384_returns_hex_digest` and SCN001 pass. Digests independently recomputed with `hashlib` and they match. |
| AC2 | UTF-8 encoding of `Zoë` (U+00EB) | Pass | Same implementation, with `.encode("utf-8")` and no normalization. `test_greeting_sha384_hashes_utf8_encoding` and SCN002 pass. `b40fde84…09051d` was confirmed independently. |
| AC3 | `""`, `" \t"`, `None`, `42` raise `ValueError("name must not be blank")` | Pass | `greet(name)` runs before hashing. `test_greeting_sha384_rejects_invalid_names` (4 cases) and SCN003 pass. |
| AC4 | Export, README docs, unchanged CLI | Pass | `src/nmg_sdlc_smoke/__init__.py` has the self-aliased import and the `__all__` entry after `greeting_sha256`. The README has the import, the example, and the exact design prose line. SCN004 runs the README block through a subprocess with output `(0, digest\n, "")`, checks that the prior exports are a subset, and gets `main(["Ada"])` → `(0, "Hello, Ada\n")`. `nmg-smoke Ada` prints `Hello, Ada\n` and exits 0. |

### Functional Requirements

| FR | Status | Evidence |
|----|--------|----------|
| FR1 | Pass | `greet.py:103-104` matches the design expression exactly |
| FR2 | Pass | `ValueError` from `greet` propagates unchanged |
| FR3 | Pass | Export added and no existing export removed (`PRIOR_EXPORTS ⊆ __all__` assertion) |
| FR4 | Pass | `README.md` import list, example, and prose line |
| FR5 | Pass | The diff touches only additive lines in `greet.py` and `__init__.py`. `cli.py` is unchanged and the full suite is green. |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Implement, export, and document greeting_sha384 | Complete | Placement matches the design: after `greeting_sha512` in `greet.py`, after `greeting_sha256` in `__init__.py` and in the README import list, and after the `greeting_sha512` example and prose in the README |
| T002 | pytest unit tests | Complete | `tests/test_greet.py`: 3 parametrized digests with a `type is str` check, a hashlib equivalence test, 4 invalid names, and an export test. `-k greeting_sha384`: 9 passed |
| T003 | Four AC-linked pytest-bdd scenarios | Complete | `tests/features/add_greeting_sha384_library_helper.feature` matches `feature.gherkin`. `tests/features/steps/test_greeting_sha384_steps.py`: 4 passed |

Release bookkeeping: `VERSION` 3.56.0 → 3.57.0, and the `CHANGELOG.md` `[3.57.0]` entry was added with released history intact. `pyproject.toml` still reads `VERSION` dynamically.

---

## Architecture Assessment

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 5 | The helper composes `greet` with hashing and does nothing else |
| Open/Closed | 5 | Purely additive. No existing helper was modified |
| Liskov Substitution | 5 | N/A (no inheritance); the signature matches its sibling helpers |
| Interface Segregation | 5 | Minimal single-function public API |
| Dependency Inversion | 5 | Library depends only on the stdlib `hashlib` (already imported) and has no CLI/test coupling |

### Layer Separation

The library stays pure and the CLI is untouched, so the boundaries in the structure steering hold.

### Dependency Flow

No new imports, modules, or runtime dependencies were added. Test-only dependencies stay in the `dev` extra.

---

## Security Assessment

- [x] Authentication: N/A
- [x] Authorization: N/A
- [x] Input validation: delegated to `greet` (rejects blank and non-string input)
- [x] Injection prevention: no shell, eval, or I/O in the library. The BDD subprocess runs the README block through `sys.executable -c` with no shell.
- [x] Data protection: SHA-384 is used as a deterministic fingerprint, not for secret storage. No secrets are involved.

## Performance Assessment

- [x] Async patterns: N/A (synchronous pure function)
- [x] Caching: N/A
- [x] Resource management: no resources held
- [x] Query optimization: N/A. The cost is O(len(greeting)).

## Testability and Error Handling

The function is pure and deterministic, and it is tested through both the public package root and pytest-bdd. Error handling reuses the single `ValueError("name must not be blank")` contract with exact-message assertions.

---

## Test Coverage

### BDD Scenarios

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 | Yes (SCN001) | Yes | Yes |
| AC2 | Yes (SCN002) | Yes | Yes |
| AC3 | Yes (SCN003) | Yes | Yes |
| AC4 | Yes (SCN004) | Yes | Yes |

### Test Results

These ran in an isolated venv (`python -m pip install -e ".[dev]"`, Python 3.14.7, which satisfies ≥3.12):

| Command | Result |
|---------|--------|
| `python -m pytest` | 756 passed, 2 skipped, 3 warnings |
| `python -m pytest tests/features` | 255 passed, 2 skipped, 3 warnings |
| `python -m ruff check .` | All checks passed |
| `python -m pytest tests/test_greet.py -k greeting_sha384` | 9 passed |
| `python -m pytest tests/features/steps/test_greeting_sha384_steps.py` | 4 passed |

The 2 skips and 3 warnings come from earlier work, not this change. The skips are issue #85 scenarios that need parent-run evidence. The warnings are `PytestUnknownMarkWarning` for `@AC1`–`@AC3` tags in older feature files. Neither involves #260.

## Exercise Test Results

This change touches no plugin files (`workflows/` or `agents/`), so exercise testing does not apply.

---

## Fixes Applied

None. No findings required fixes.

## Remaining Issues

None.

---

## Positive Observations

- The implementation matches the design's code block character for character, and it is placed exactly where the spec says.
- The BDD AC4 step executes the real README example instead of string-matching it. It also guards the prior exports against removal.
- Digests were confirmed independently against `hashlib` outside the test suite.

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/greet.py` | 0 | |
| `src/nmg_sdlc_smoke/__init__.py` | 0 | |
| `README.md` | 0 | |
| `CHANGELOG.md` | 0 | |
| `VERSION` | 0 | |
| `tests/test_greet.py` | 0 | |
| `tests/features/add_greeting_sha384_library_helper.feature` | 0 | |
| `tests/features/steps/test_greeting_sha384_steps.py` | 0 | |

---

## Recommendation

**Ready for PR**

All 4 ACs, 5 FRs, 3 tasks, and 4 scenarios pass at head `3e112065d688be81a4f064d052f921b1b7d6d332`. The required local checks are green, and the steering gate is complete with no ceiling.
