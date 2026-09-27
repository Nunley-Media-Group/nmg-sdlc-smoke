# Verification Report: Add nmg-smoke --lowercase flag

**Date**: 2026-09-27
**Issue**: #188
**Reviewer**: architecture-reviewer (nmg-sdlc verify worker)
**Scope**: Implementation verification against spec
**Verification head**: ae7466d54f9d0814be80911215dd67d5c52e2aa9

---

## Executive Summary

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

All six acceptance criteria and five functional requirements are implemented and covered by unit tests and one-to-one pytest-bdd scenarios. All registered checks pass on Python 3.12.12 and 3.14.7. The deterministic steering gate is complete, has no ceiling, and declares zero validations.

---

## Deterministic Steering Artifact and Ceiling

- Runner: `sdlc-verify-steering.mjs --project . --issue 188 --spec specs/188-add-nmg-smoke-lowercase-flag --base main --controller-run-id 2b6696c4-dca1-4953-9deb-970dc0861bc4`
- Artifact: `.omp/sdlc/verification/188.json`
- Identity: head `ae7466d54f9d0814be80911215dd67d5c52e2aa9`, steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`, spec `sha256:0258b327eed50410d2b9646f2f6dce9247dba9d60b44e6a70bdedc6fb30d2f13`
- Result: `ok: true`, `ceiling: null`
- Coverage: `declared: 0`, `recorded: 0`, `complete: true`, no missing, duplicate, or unknown ids
- `steering/manifest.json` has 4 modules, 3 snippets, 0 extensions, and `validations: []`. No `repository.nmg-sdlc-smoke` or `project.nmg-sdlc-smoke` validation is registered, so the real smoke lifecycle requirement does not apply to this gate.

---

## Issue Scope

- Active issue: #188
- Spec: `specs/188-add-nmg-smoke-lowercase-flag`
- Manifest: `implicit single issue`
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6]; FR [FR1, FR2, FR3, FR4, FR5]; tasks [T001, T002, T003, T004]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":188,"specPath":"specs/188-add-nmg-smoke-lowercase-flag","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5"],"tasks":["T001","T002","T003","T004"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Pass
- PR evidence: Not required

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `--lowercase Ada` prints `hello, ada` + LF, empty stderr, exit 0 | Pass | `src/nmg_sdlc_smoke/cli.py:41-42`. Unit test `test_cli_prints_lowercase_greeting` covers both argument orders. SCN001 passes. Installed script printed `hello, ada` with rc=0. |
| AC2 | Composes with prefix/parentheses/repeat/no-newline; prefix not lowercased | Pass | Casing runs before `args.prefix +` (`cli.py:39-43`). `test_cli_lowercase_composes_before_prefix_and_wrappers` and SCN002 pass. `od -c` shows `(OK: hello, ada)\n(OK: hello, ada)` with no final LF. |
| AC3 | `str.lower` semantics for `ÅSA` and `Straße` | Pass | `message.lower()` is used, not `casefold`. `test_cli_lowercase_uses_str_lower_semantics` and SCN003 pass. Installed script printed `hello, åsa` and `hello, straße`. |
| AC4 | Combining with `--uppercase` exits 2, stderr contains `not allowed with argument`, empty stdout | Pass | `parser.add_mutually_exclusive_group()` is at `cli.py:20-22`. `test_cli_rejects_uppercase_with_lowercase` covers both orders, and SCN004 passes. Installed script printed `argument --lowercase: not allowed with argument --uppercase` with rc=2. |
| AC5 | `--lowercase " "` exits 1 with blank-name error, empty stdout | Pass | The existing `greet` validation still runs before casing (`cli.py:34-37`). `test_cli_rejects_blank_name_with_lowercase` covers `""`, `" "`, `"\t"`, and `"\n"`. SCN005 passes, and the installed script returned rc=1. |
| AC6 | Default and `--uppercase` output unchanged; `--help` lists `--lowercase` | Pass | Existing CLI tests and SCN006 pass. The installed script printed `Hello, Ada` and `HELLO, ADA`, and help usage shows `[--uppercase \| --lowercase]`. README documents the flag at `README.md:145-154`. |

| FR | Status | Evidence |
|----|--------|----------|
| FR1 | Pass | `case.add_argument("--lowercase", action="store_true")` is long-only and boolean. |
| FR2 | Pass | The `elif args.lowercase` branch sits at the `--uppercase` stage, before prefix, wrappers, and the repeat loop. |
| FR3 | Pass | An argparse mutually exclusive group returns exit 2 in either order. |
| FR4 | Pass | The full pre-existing suite passes unchanged (427 passed). |
| FR5 | Pass | The README CLI section includes an example, `str.lower()`/prefix ordering, and the exit-2 exclusion. |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add the mutually exclusive --lowercase flag | Complete | Only `cli.py` changed (+5/-1). No new module, helper, or dependency. |
| T002 | Add focused CLI unit tests | Complete | Six test functions (12 cases) in `tests/test_cli.py`. |
| T003 | Add pytest-bdd acceptance scenarios | Complete | The feature body matches `feature.gherkin` exactly (diffed). Steps resolve the script via `sysconfig.get_path("scripts")` with `.exe` fallback and use `encoding="utf-8"` and `PYTHONIOENCODING=utf-8`. |
| T004 | Document --lowercase in the README | Complete | Added directly after the `--uppercase` example. No other README content changed. |

---

## Architecture Assessment

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 5 | Casing stays in the CLI adapter, and `greet` remains pure. |
| Open/Closed | 5 | Additive branch. Existing flags are untouched. |
| Liskov Substitution | 5 | N/A: no type hierarchy. |
| Interface Segregation | 5 | One long-only boolean flag. |
| Dependency Inversion | 5 | The CLI depends on the library, not the reverse. |

### Layer Separation

The library (`greet.py`, `__init__.py`) is unchanged. The CLI is a thin argparse adapter, as the structure steering requires.

### Dependency Flow

The dependency direction is `cli -> greet`. No runtime dependencies were added.

---

## Security Assessment

- [x] Authentication: N/A (local CLI)
- [x] Authorization: N/A
- [x] Input validation: argparse enforces mutual exclusion, and blank names are rejected by `greet`
- [x] Injection prevention: no shell, file, or eval use. Test subprocesses use argv lists with `shell=False`.
- [x] Data protection: N/A

## Performance Assessment

- [x] Async patterns: N/A
- [x] Caching: N/A
- [x] Resource management: a single `str.lower()` call on a short string
- [x] Query optimization: N/A

## Testability and Error Handling

- Testability (5): `main(argv)` is injectable. Unit tests use `capsys`, and BDD scenarios exercise the installed console script. Tests are deterministic and isolated.
- Error handling (5): usage errors go through argparse (exit 2, stderr). Validation errors keep the existing `parser.exit(1, ...)` path, and no exceptions are swallowed.

---

## Test Coverage

### BDD Scenarios

| Acceptance Criterion | Has Scenario | Has Steps | Passes |
|---------------------|-------------|-----------|--------|
| AC1 | Yes (SCN001) | Yes | Yes |
| AC2 | Yes (SCN002) | Yes | Yes |
| AC3 | Yes (SCN003) | Yes | Yes |
| AC4 | Yes (SCN004) | Yes | Yes |
| AC5 | Yes (SCN005) | Yes | Yes |
| AC6 | Yes (SCN006) | Yes | Yes |

### Test Results

Each run used an isolated temporary venv with `pip install -e ".[dev]"`:

| Command | Python 3.12.12 | Python 3.14.7 |
|---------|----------------|---------------|
| `python -m pytest` | 427 passed, 2 skipped | 427 passed, 2 skipped |
| `python -m pytest tests/features` | 159 passed, 2 skipped | 159 passed, 2 skipped |
| `python -m ruff check .` | All checks passed | All checks passed |
| `pytest -k lowercase` (unit + BDD subset) | — | 18 passed |

The 2 skips are pre-existing issue #85 scenarios ("requires parent-run issue 85 verification evidence") and are unrelated to #188. The warnings are third-party deprecations from `gherkin` and `pytest_bdd`.

### Real CLI Smoke

These results came from running the installed `nmg-smoke` directly:
- `--lowercase Ada` printed `hello, ada` (rc=0).
- `--lowercase ÅSA` printed `hello, åsa` (rc=0).
- `--lowercase Straße` printed `hello, straße` (rc=0).
- `--uppercase --lowercase Ada` printed a usage error with `not allowed with argument --uppercase` (rc=2).
- `Ada` printed `Hello, Ada` and `--uppercase Ada` printed `HELLO, ADA` (rc=0).
- `--lowercase " "` printed `nmg-smoke: error: name must not be blank` (rc=1).

## Exercise Test Results

Not applicable. The change touches no plugin files (`workflows/`, `agents/`). This repository is a Python smoke host.

---

## Fixes Applied

None required.

## Remaining Issues

None.

---

## Positive Observations

- The design uses the standard-library argparse mutually exclusive group instead of custom validation.
- The feature file is byte-identical to the approved `feature.gherkin` body.
- Non-ASCII subprocess output is pinned to UTF-8 on every platform.

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/cli.py` | 0 | Mutually exclusive group and `elif` lowercase branch |
| `tests/test_cli.py` | 0 | 12 new parametrized cases |
| `tests/features/add_nmg_smoke_lowercase_flag.feature` | 0 | SCN001–SCN006 |
| `tests/features/steps/test_lowercase_steps.py` | 0 | Installed-script subprocess steps |
| `README.md` | 0 | CLI docs for `--lowercase` |

---

## Recommendation

**Ready for PR**

Every delivery AC, FR, task, and scenario passes locally at the verification head. The deterministic gate is complete with no ceiling, and no PR-only evidence is required.
