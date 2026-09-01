# Tasks: Add nmg-smoke --uppercase flag

**Issue**: #43
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Summary

| Phase | Tasks | Status |
|-------|-------|--------|
| CLI | 1 | [ ] |
| Verification | 2 | [ ] |
| Docs | 1 | [ ] |
| **Total** | 4 | |

---

## Phase 1: CLI

### T001: Add argparse --uppercase and uppercase successful greeting

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `parser.add_argument("--uppercase", action="store_true")` is present; no short `-u`; dest remains `uppercase`
- [ ] `parser.add_argument("name")` stays required (no `nargs="?"`)
- [ ] After successful `greet`, the CLI does `print(message.upper() if args.uppercase else message)`
- [ ] `ValueError` path stays `parser.exit(1, f"nmg-smoke: error: {error}\n")` with no stdout greeting
- [ ] `src/nmg_sdlc_smoke/greet.py` and `src/nmg_sdlc_smoke/__init__.py` are untouched
- [ ] No new runtime dependency

**Notes**: If `cli.py` already has `--version` or other arguments from a previously delivered spec, add `--uppercase` beside them and do not change those behaviors. Do not introduce a library helper for uppercase.

---

## Phase 2: Verification

### T002: Unit tests for uppercase and unchanged CLI

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `main(["--uppercase", "Ada"]) == 0` and stdout is `HELLO, ADA\n` with empty stderr
- [ ] `main(["Ada", "--uppercase"]) == 0` and stdout is `HELLO, ADA\n` with empty stderr
- [ ] Existing `test_cli_prints_greeting` still expects `main(["Ada"]) == 0` and `Hello, Ada\n`
- [ ] `main(["--uppercase"])` raises `SystemExit` with non-zero code and empty stdout
- [ ] Parametrized blank names `""`, `" "`, `"\t"`, `"\n"` with `--uppercase` raise `SystemExit` code `1`, empty stdout, and `name must not be blank` on stderr
- [ ] `tests/test_greet.py` is untouched
- [ ] `python -m pytest tests/test_cli.py tests/test_greet.py` exits 0

### T003: pytest-bdd feature and steps for AC1–AC5

**File(s)**: `tests/features/add_nmg_smoke_uppercase_flag.feature`, `tests/features/steps/test_uppercase_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec `**Issue**` / `**Date**` / `**Status**` / `**Author**` header lines
- [ ] Scenarios `@SCN001`–`@SCN005` map 1:1 to AC1–AC5
- [ ] Steps call `nmg_sdlc_smoke.cli.main` in-process with `capsys`, matching `tests/features/steps/test_greeting_steps.py`
- [ ] `scenarios("../add_nmg_smoke_uppercase_flag.feature")` lives only in `test_uppercase_steps.py`
- [ ] New step module does not redefine step texts already defined in `test_greeting_steps.py`
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document nmg-smoke --uppercase in README CLI

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] The existing `nmg-smoke Ada` / `Hello, Ada` example remains
- [ ] CLI section documents `nmg-smoke --uppercase Ada` printing `HELLO, ADA`
- [ ] Library section still documents only the existing `greet` example (no uppercase parameter)

---

## Dependency Graph

```
T001 ──┬──▶ T002 ──▶ T003
       └──▶ T004
```

---

## Delivery Evidence

- Registered managed steering runtime alignment: the CLI-only presentation change follows `steering/manifest.json` and the registered product, technology, structure, and verification guidance; no steering artifact change is required.
- Behavior for `VERSION`: deterministic delivery advances the existing 3.x release metadata while `pyproject.toml` continues to read `VERSION` dynamically; the runtime dependency and public-library contracts remain unchanged.

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #43 | 2026-09-01 | Initial feature spec |

---

## Validation Checklist

Before moving to IMPLEMENT phase:

- [x] Each task has single responsibility
- [x] Dependencies are correctly mapped
- [x] Tasks can be completed independently (given dependencies)
- [x] Acceptance criteria are verifiable
- [x] File paths reference actual project structure
- [x] Test tasks are included
- [x] No circular dependencies
- [x] Tasks are in logical execution order
