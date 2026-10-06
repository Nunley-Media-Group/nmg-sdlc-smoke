# Verification Report: Add nmg-smoke --casefold flag

**Date**: 2026-10-06
**Issue**: #197
**Reviewer**: Codex
**Scope**: Implementation verification against spec
**Verification head**: b618061249c916a371b2dc450aab41e6fa7c5748

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

All six acceptance criteria, five functional requirements, and four tasks are satisfied at the verification head. The change is a single argparse registration plus one `elif` casing branch in `src/nmg_sdlc_smoke/cli.py`, with unit tests, pytest-bdd scenarios, and README documentation. Required steering checks (`python -m pytest`, `python -m pytest tests/features`, `python -m ruff check .`) pass, and the installed console script was exercised directly.

---

## Deterministic Steering Artifact and Ceiling

- Runner: `sdlc-verify-steering.mjs --project . --issue 197 --spec specs/197-add-nmg-smoke-casefold-flag --base main --controller-run-id ce8cec0a-f924-445e-a30c-78dbc3d87a38`
- Artifact: `.omp/sdlc/verification/197.json`
- Identity: head `b618061249c916a371b2dc450aab41e6fa7c5748`, steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`, spec `sha256:48f16a73b19a29082739aa86396b8393d538c7a76657ada7c69b9d0fd28840d0`
- Result: `ok: true`, `ceiling: null`
- Coverage: `declared: 0`, `recorded: 0`, `complete: true`, no missing/duplicate/unknown results
- `steering/manifest.json` registers no `validations`, so no `repository.nmg-sdlc-smoke` or `project.nmg-sdlc-smoke` provider applies; the gate is complete with no project-specific validations.

---

## Issue Scope

- Active issue: #197
- Spec: `specs/197-add-nmg-smoke-casefold-flag`
- Manifest: `implicit single issue`
- Resolver status: `implicit_single_issue`
- Delivery: AC [AC1, AC2, AC3, AC4, AC5, AC6]; FR [FR1, FR2, FR3, FR4, FR5]; tasks [T001, T002, T003, T004]; scenarios [SCN001, SCN002, SCN003, SCN004, SCN005, SCN006]
- Regression: AC []; FR []; scenarios []

<!-- nmg-sdlc-issue-scope: {"issueNumber":197,"specPath":"specs/197-add-nmg-smoke-casefold-flag","status":"implicit_single_issue","delivery":{"acceptanceCriteria":["AC1","AC2","AC3","AC4","AC5","AC6"],"functionalRequirements":["FR1","FR2","FR3","FR4","FR5"],"tasks":["T001","T002","T003","T004"],"scenarios":["SCN001","SCN002","SCN003","SCN004","SCN005","SCN006"]},"regression":{"acceptanceCriteria":[],"functionalRequirements":[],"scenarios":[]}} -->

## Delivery Validation

- Local verification: Pass
- PR evidence: Not required

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `--casefold Straße` → `hello, strasse\n`, empty stderr, exit 0 | Pass | `src/nmg_sdlc_smoke/cli.py:25,50-51`; `tests/test_cli.py::test_cli_prints_casefold_greeting` (both argument orders); SCN001; installed script printed `hello, strasse\n`, rc=0 |
| AC2 | `ADA` → `hello, ada`; `ΣΊΣΥΦΟΣ` → `hello, σίσυφοσ` | Pass | `str.casefold()` at `cli.py:51`; `test_cli_casefold_uses_str_casefold_semantics`; SCN002; installed script output matched byte-for-byte, rc=0 |
| AC3 | Composes with `--prefix 'OK: ' --quotes --repeat 2 --no-newline` | Pass | Casing (`cli.py:42-51`) precedes prefix/wrappers/loop (`cli.py:52-61`); `test_cli_casefold_composes_before_prefix_and_wrappers`; SCN003; installed script printed `"OK: hello, strasse"\n"OK: hello, strasse"` with no final LF |
| AC4 | Combining with any other case flag, either order, exits 2 | Pass | `--casefold` registered in the `case` mutually exclusive group (`cli.py:20-25`); 8 parametrized cases in `test_cli_rejects_casefold_with_other_case_flag`; SCN004; installed script: all 8 combinations rc=2 with `not allowed with argument`, empty stdout |
| AC5 | Blank name with `--casefold` exits 1 with blank-name error | Pass | Existing `greet` validation path (`cli.py:37-40`) runs before casing; `test_cli_rejects_blank_name_with_casefold` (`""`, `" "`, `"\t"`, `"\n"`); SCN005; installed script rc=1 with `nmg-smoke: error: name must not be blank` |
| AC6 | Default/lowercase output preserved; help lists `--casefold` | Pass | `test_cli_help_lists_casefold`, existing default/lowercase tests; SCN006; installed script printed `Hello, Ada\n` and `hello, straße\n`; `--help` lists `--casefold` |

### Functional Requirements

| FR | Status | Evidence |
|----|--------|----------|
| FR1 | Pass | Long-only `store_true` `--casefold`; `message.casefold()` applied to `greet(name)` result |
| FR2 | Pass | `elif args.casefold` sits in the casing chain before `args.prefix + message`, wrappers, and the repeat/newline loop |
| FR3 | Pass | Same argparse mutually exclusive group; no custom validation code |
| FR4 | Pass | Only additive changes in `cli.py`; full suite (495 passed) including pre-existing CLI tests unchanged |
| FR5 | Pass | `README.md` CLI section documents example, `str.casefold()` semantics, prefix ordering, and exit-2 mutual exclusion directly after `--titlecase` |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add the mutually exclusive `--casefold` flag | Complete | Registered directly after `--titlecase`; `elif` after the titlecase branch; no new module or dependency |
| T002 | Add focused CLI unit tests | Complete | 18 casefold unit cases in `tests/test_cli.py`, all passing |
| T003 | Add pytest-bdd acceptance scenarios | Complete | Feature body is identical to `specs/197-add-nmg-smoke-casefold-flag/feature.gherkin`; steps resolve the installed script via `sysconfig.get_path("scripts")` with `encoding="utf-8"` and `PYTHONIOENCODING=utf-8`; issue #90 casefold helper feature/steps unchanged |
| T004 | Document `--casefold` in the README | Complete | Section added after `--titlecase` text; other docs unchanged |

---

## Architecture Assessment

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 5 | CLI adapter owns parsing and rendering; library untouched |
| Open/Closed | 5 | Additive extension of the existing case group and casing chain |
| Liskov Substitution | 5 | N/A; no type hierarchy |
| Interface Segregation | 5 | One opt-in flag; public library API unchanged |
| Dependency Inversion | 5 | CLI depends on `greet`; library has no CLI dependency |

### Layer Separation

`greet.py` and `__init__.py` are unchanged; the CLI remains a thin adapter, matching structure steering.

### Dependency Flow

CLI → library only. No runtime dependencies added; `pyproject.toml` unchanged.

---

## Security Assessment

- [x] Authentication: N/A (local CLI)
- [x] Authorization: N/A
- [x] Input validation: name validated by existing `greet`; flag is boolean
- [x] Injection prevention: no shell, file, or eval usage; BDD steps call `subprocess.run` with an argument list
- [x] Data protection: no sensitive data handled

---

## Performance Assessment

- [x] Async patterns: N/A
- [x] Caching: N/A
- [x] Resource management: no new resources
- [x] Query optimization: N/A; single O(n) string operation

---

## Error Handling

Mutual exclusion is delegated to argparse (exit 2 usage error); blank names keep the existing `parser.exit(1, ...)` path before casing. No new error paths or swallowed exceptions.

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

### Coverage Summary

- Feature files: 6 scenarios in `tests/features/add_nmg_smoke_casefold_flag.feature`
- Step definitions: Implemented in `tests/features/steps/test_casefold_flag_steps.py`
- Unit tests: 18 casefold cases in `tests/test_cli.py`
- Integration tests: BDD steps exercise the installed console script as a subprocess

### Commands (isolated venv, `python -m pip install -e ".[dev]"`, Python 3.14.7)

| Command | Result |
|---------|--------|
| `python -m pytest` | 495 passed, 2 skipped |
| `python -m pytest tests/features` | 177 passed, 2 skipped |
| `python -m ruff check .` | All checks passed |
| `python -m pytest tests/test_cli.py -k casefold tests/features/steps/test_casefold_flag_steps.py` | 24 passed |

The 2 skips are pre-existing issue #85 scenarios (`requires parent-run issue 85 verification evidence`); the `PytestUnknownMarkWarning` for `AC1`–`AC3` comes from pre-existing feature tags. Neither is touched by this change.

### Installed Console Script Smoke

| Invocation | Observed |
|------------|----------|
| `nmg-smoke --casefold Straße` | `hello, strasse\n`, rc=0 |
| `nmg-smoke --casefold ADA` | `hello, ada\n`, rc=0 |
| `nmg-smoke --casefold ΣΊΣΥΦΟΣ` | `hello, σίσυφοσ\n`, rc=0 |
| `nmg-smoke --casefold --prefix 'OK: ' --quotes --repeat 2 --no-newline Straße` | `"OK: hello, strasse"\n"OK: hello, strasse"`, rc=0 |
| `--casefold` with each of `--uppercase/--lowercase/--swapcase/--titlecase`, both orders | 8/8 rc=2, `not allowed with argument`, empty stdout |
| `nmg-smoke --casefold " "` | rc=1, `nmg-smoke: error: name must not be blank` |
| `nmg-smoke Ada` / `nmg-smoke --lowercase Straße` | `Hello, Ada\n` / `hello, straße\n`, rc=0 |
| `nmg-smoke --help` | lists `--casefold` |

---

## Fixes Applied

| Severity | Category | Location | Original Issue | Fix Applied | Routing |
|----------|----------|----------|----------------|-------------|---------|
| — | — | — | None required | — | — |

## Remaining Issues

None.

---

## Positive Observations

- Minimal, spec-exact change reusing the argparse mutually exclusive group.
- BDD steps use the installed script with explicit UTF-8 handling, so non-ASCII arguments behave identically across platforms.
- Tests cover both argument orders for every exclusive pair and all blank-name variants.

---

## Recommendations Summary

### Before PR (Must)
- None

### Short Term (Should)
- None

### Long Term (Could)
- None

---

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/cli.py` | 0 | Flag registration and casing branch |
| `tests/test_cli.py` | 0 | Casefold unit tests |
| `tests/features/add_nmg_smoke_casefold_flag.feature` | 0 | Matches approved gherkin |
| `tests/features/steps/test_casefold_flag_steps.py` | 0 | Subprocess steps |
| `README.md` | 0 | `--casefold` documentation |

---

## Recommendation

**Ready for PR**

Every approved AC, FR, task, and scenario is satisfied with passing local tests, lint, and direct console-script evidence; the registered steering gate is complete with no declared validations.
