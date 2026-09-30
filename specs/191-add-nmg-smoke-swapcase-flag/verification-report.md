# Verification Report: Add nmg-smoke --swapcase flag

**Date**: 2026-09-30
**Issue**: #191
**Reviewer**: Codex
**Scope**: Implementation verification against spec

**Verification head**: abe52e56a0e0d3f7c61dead9e149f6c1ac8391af

---

## Executive Summary

Commit `abe52e5` (`feat: add nmg-smoke --swapcase flag (#191)`) implements the approved spec. `--swapcase` is registered in the existing mutually exclusive `case` group in `src/nmg_sdlc_smoke/cli.py`, and a single `elif args.swapcase` branch applies `str.swapcase()` at the same stage as `--uppercase`/`--lowercase`, before prefix, wrappers, repetition, and newline handling. All six delivery acceptance criteria pass: unit tests cover them, pytest-bdd scenarios SCN001–SCN006 cover them, and direct runs of the installed console script confirm them. All required steering checks are green. `steering/manifest.json` declares no project validations, so deterministic coverage is complete with zero declarations.

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
**Total Issues**: 1 (Low, cosmetic, non-blocking)

---

## Deterministic Steering Artifact and Ceiling

- Runner: `sdlc-verify-steering.mjs --project . --issue 191 --spec specs/191-add-nmg-smoke-swapcase-flag --base main --controller-run-id b80da6ff-53ea-4367-8832-20a2c38ea7d1`
- Artifact: `.omp/sdlc/verification/191.json` (`ok: true`)
- Identity: head `abe52e56a0e0d3f7c61dead9e149f6c1ac8391af`, steering `sha256:96bcc8489c8cf612473fd4847d1341aad49d59dc42286b0252d26613318aa4cf`, spec `sha256:7d1c27662c00d7401faac7b7b381f603c7716b2e72c9db1a733b449ce11c362b`
- Ceiling: `null`
- Coverage: declared 0, recorded 0, complete `true`; missing/duplicate/unknown are all empty
- `steering/manifest.json` registers `validations: []`. `repository.nmg-sdlc-smoke` and `project.nmg-sdlc-smoke` are not declared, so no real smoke lifecycle evidence is required.
- Changed paths vs `main`: `README.md`, `specs/191-add-nmg-smoke-swapcase-flag/verification-report.md`, `src/nmg_sdlc_smoke/cli.py`, `tests/features/add_nmg_smoke_swapcase_flag.feature`, `tests/features/steps/test_swapcase_steps.py`, `tests/test_cli.py`

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

- Local verification: Pass
- PR evidence: Not required

---

## Acceptance Criteria Verification

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC1 | `nmg-smoke --swapcase Ada` prints `hELLO, aDA\n` with empty stderr and exit 0 | Pass | `src/nmg_sdlc_smoke/cli.py:23,44-45`. `tests/test_cli.py:325-334` covers both argument orders, and SCN001 passes. The installed script prints `hELLO, aDA\n` and exits 0. |
| AC2 | Composes with `--prefix 'OK: ' --parentheses --repeat 2 --no-newline ADA` and the prefix keeps its case | Pass | The swap happens at `cli.py:44-45` before the prefix at `cli.py:46`. `tests/test_cli.py:337-352` and SCN002 pass. The installed script prints `(OK: hELLO, ada)\n(OK: hELLO, ada)` with no final LF and exits 0. |
| AC3 | `ÅSA` → `hELLO, åsa\n` and `Straße` → `hELLO, sTRASSE\n` | Pass | `str.swapcase()` at `cli.py:45`. `tests/test_cli.py:355-364` and SCN003 (UTF-8 subprocess) pass. The installed script produces exactly these bytes and exits 0 for both names. |
| AC4 | Combining `--swapcase` with `--uppercase` or `--lowercase` in either order exits 2 with `not allowed with argument` and empty stdout | Pass | The flag is in the `case` mutually exclusive group (`cli.py:20-23`). `tests/test_cli.py:367-385` covers all four orders, and SCN004 passes. Installed example: `argument --uppercase: not allowed with argument --swapcase`, exit 2. |
| AC5 | `nmg-smoke --swapcase " "` exits 1 with `nmg-smoke: error: name must not be blank` and empty stdout | Pass | The `greet` validation path is unchanged (`cli.py:36-39`). `tests/test_cli.py:388-398` covers `""`, `" "`, `"\t"`, and `"\n"`, and SCN005 passes. The installed script exits 1 with the exact error. |
| AC6 | Default, `--uppercase`, and `--lowercase` output are unchanged, and `--help` lists `--swapcase` | Pass | The installed script prints `Hello, Ada\n`, `HELLO, ADA\n`, and `hello, ada\n`. Usage shows `[--uppercase \| --lowercase \| --swapcase]`. `tests/test_cli.py:401-406` and SCN006 pass, and the existing uppercase/lowercase tests still pass. |

### Functional Requirements

| FR | Status | Evidence |
|----|--------|----------|
| FR1 | Pass | Long-only `store_true` `--swapcase` flag; `message.swapcase()` applied to the `greet(name)` result |
| FR2 | Pass | The `elif` chain at `cli.py:40-45` runs before prefix, parentheses, braces, quotes, and the repeat/newline loop. AC2 shows the prefix and wrappers are not swapped. |
| FR3 | Pass | Same `case` group as `--uppercase`/`--lowercase`; argparse exits 2 in both orders |
| FR4 | Pass | The only changes are the added argument and `elif` branch. Full suite: 447 passed, including all pre-existing CLI contracts. |
| FR5 | Pass | `README.md:156-165` documents the example, the `str.swapcase()` semantics, that the prefix keeps its case, and that combining with another case flag exits 2 |

---

## Task Completion

| Task | Description | Status | Notes |
|------|-------------|--------|-------|
| T001 | Add mutually exclusive `--swapcase` flag | Complete | Registered directly after `--lowercase` (`cli.py:23`), with an `elif` after the lowercase check (`cli.py:44-45`). No new module, helper, or dependency. |
| T002 | Focused CLI unit tests | Complete | 14 parametrized cases in `tests/test_cli.py:325-406` match every listed acceptance bullet |
| T003 | pytest-bdd acceptance scenarios | Complete | `tests/features/add_nmg_smoke_swapcase_flag.feature` scenario content is identical to `feature.gherkin` (SCN001–SCN006). Steps resolve `nmg-smoke`/`nmg-smoke.exe` via `sysconfig.get_path("scripts")` and run with UTF-8 I/O. |
| T004 | README documentation | Complete | Placed directly after the `--lowercase` documentation in `## CLI`. The rest of the README is unchanged. |

---

## Architecture Assessment

### SOLID Compliance

| Principle | Score (1-5) | Notes |
|-----------|-------------|-------|
| Single Responsibility | 5 | `greet.py` stays pure and untouched. `cli.py` still owns parsing and rendering only. |
| Open/Closed | 5 | Extends the existing case group and `if/elif` chain without modifying existing branches |
| Liskov Substitution | 5 | Not applicable; there is no inheritance |
| Interface Segregation | 5 | The public library API is unchanged (out of scope, as required) |
| Dependency Inversion | 5 | The CLI depends on the library. The library has no dependency on the CLI, tests, or layout. |

### Layer Separation

Compliant with structure steering: the library does not import the CLI, and the change adds no utility module, service layer, or alias.

### Dependency Flow

`cli.py` → `greet.py` only. No runtime dependencies were added (`pyproject.toml` is unchanged).

---

## Security Assessment

- [x] Authentication: N/A (local CLI)
- [x] Authorization: N/A
- [x] Input validation: argparse enforces mutual exclusion, and `greet` rejects blank names before any transform
- [x] Injection prevention: no shell, eval, or file I/O. The BDD steps call `subprocess.run` with an argv list and no shell.
- [x] Data protection: N/A

## Performance Assessment

- [x] Async patterns: N/A
- [x] Caching: N/A
- [x] Resource management: one O(n) `str.swapcase()` over the greeting; no resources held
- [x] Query optimization: N/A

## Testability Assessment

The pure `main(argv)` entry point is unit-tested with `capsys`. The installed console-script path is exercised in subprocess BDD steps. The tests are deterministic, isolated, and full-suite safe, and they assert on exact behavior (exact bytes, exit codes, stderr substrings).

## Error Handling Assessment

Usage errors use argparse's exit 2. Blank names keep the existing `parser.exit(1, "nmg-smoke: error: ...")` path. No stdout is written on either error path, as AC4 and AC5 verify.

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

### Test Execution (isolated venv, `python -m pip install -e ".[dev]"`, Python 3.14.7)

| Command | Result |
|---------|--------|
| `python -m pytest` | Exit 0; 447 passed, 2 skipped |
| `python -m pytest tests/features` | Exit 0; 165 passed, 2 skipped |
| `python -m ruff check .` | Exit 0; All checks passed |
| `python -m pytest tests/test_cli.py tests/features/steps/test_swapcase_steps.py -k swapcase` | 20 passed (14 unit + 6 BDD) |

The 2 skips are pre-existing issue #85 scenarios gated on parent-run evidence (`requires parent-run issue 85 verification evidence`). They are unrelated to #191.

### Installed Console-Script Smoke

Each case was run directly against the venv's `nmg-smoke` with `PYTHONIOENCODING=utf-8`, and stdout was checked byte-for-byte with `od -c`:

- `--swapcase Ada` → `hELLO, aDA\n`, exit 0
- `--swapcase --prefix 'OK: ' --parentheses --repeat 2 --no-newline ADA` → `(OK: hELLO, ada)\n(OK: hELLO, ada)`, exit 0
- `--swapcase ÅSA` → `hELLO, åsa\n`; `--swapcase Straße` → `hELLO, sTRASSE\n`, exit 0
- `--swapcase --uppercase Ada` and `--lowercase --swapcase Ada` → exit 2, `not allowed with argument`, empty stdout
- `--swapcase " "` → exit 1, `nmg-smoke: error: name must not be blank`
- `Ada` / `--uppercase Ada` / `--lowercase Ada` → `Hello, Ada\n` / `HELLO, ADA\n` / `hello, ada\n`, and `--help` lists `--swapcase`

### Exercise Testing

Not applicable. The change touches no plugin `workflows/` or `agents/` files, because this repository is a Python host.

---

## Fixes Applied

| Severity | Category | Location | Original Issue | Fix Applied | Routing |
|----------|----------|----------|----------------|-------------|---------|
| — | — | `specs/191-add-nmg-smoke-swapcase-flag/verification-report.md` | The committed report described the pre-implementation head `d533a4e` | Regenerated this report at the implementation head `abe52e5` | direct |

## Remaining Issues

### Critical Issues

None.

### High Priority

None.

### Medium Priority

None.

### Low Priority

| Field | Value |
|-------|-------|
| **Severity** | Low |
| **Category** | Style |
| **Location** | `tests/test_cli.py:407-409` |
| **Issue** | Three blank lines separate `test_cli_help_lists_swapcase` from the next test. PEP 8 expects two. Ruff's configured rule set does not flag it. |
| **Impact** | Cosmetic only; no behavior or gate effect |
| **Reason Not Fixed** | The verify publication scope permits writing only `verification-report.md` |

---

## Positive Observations

- The implementation is minimal: 3 source lines, placed exactly where the design specifies.
- The feature file matches the approved `feature.gherkin` scenario content exactly.
- The unit tests cover both flag orders for the mutual-exclusion and argument-position cases, and every blank-name variant.

---

## Recommendations Summary

### Before PR (Must)
- None

### Short Term (Should)
- Collapse the extra blank line at `tests/test_cli.py:409` in a later touch of the file

### Long Term (Could)
- None

---

## Files Reviewed

| File | Issues | Notes |
|------|--------|-------|
| `src/nmg_sdlc_smoke/cli.py` | 0 | Flag and transform as designed |
| `tests/test_cli.py` | 1 | Low: extra blank line |
| `tests/features/add_nmg_smoke_swapcase_flag.feature` | 0 | Matches the spec gherkin |
| `tests/features/steps/test_swapcase_steps.py` | 0 | Subprocess, UTF-8, portable script resolution |
| `README.md` | 0 | FR5 satisfied |
| `steering/manifest.json` | 0 | Valid; no registered validations |

---

## Recommendation

**Ready for PR**

All delivery ACs, FRs, tasks, and scenarios pass at `abe52e56a0e0d3f7c61dead9e149f6c1ac8391af`. The required steering checks are green, and deterministic coverage is complete with a `null` ceiling.
