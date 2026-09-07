# Tasks: Add nmg-smoke --separator TEXT option

**Issue**: #98
**Date**: 2026-09-07
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

**Steering alignment**: This CLI-only change follows the registered managed steering runtime in `steering/manifest.json`; it adds no project-specific validation declaration or steering artifact change.

**VERSION ownership**: T001–T004 must not edit `VERSION` or `CHANGELOG.md`. That is the authoring/feature-implementation constraint from the issue body. Delivery/open-pr MUST still apply the normal enhancement minor bump required by `CHANGELOG.md` and `steering/snippets/project-tech.md`: `3.32.0` → `3.33.0`, add a `#98` CHANGELOG entry under Added, preserve released headings, and keep `pyproject.toml` reading VERSION dynamically. Do not write `**Version bump**: major`. Do not treat “do not bump VERSION” as a delivery skip.

---

## Phase 1: CLI

### T001: Add argparse --separator TEXT and use it between repeats

**File(s)**: `src/nmg_sdlc_smoke/cli.py`
**Type**: Modify
**Depends**: None
**Acceptance**:
- [ ] `parser.add_argument("--separator", default="\n", metavar="TEXT")` is present after `--no-newline` and before `name`; there is no short `-s`; dest remains `separator`
- [ ] `--separator` does not use `nargs="?"`
- [ ] `parser.add_argument("name")` stays required
- [ ] Existing `--uppercase`, `--repeat COUNT`, `--prefix TEXT`, and `--no-newline` parser declarations and transform order remain
- [ ] `greet(args.name)` is still called exactly once before any stdout output
- [ ] Existing `ValueError` handling stays `parser.exit(1, f"nmg-smoke: error: {error}\n")`
- [ ] The print loop becomes `for index in range(args.repeat)` with `end = args.separator` on non-final iterations and `end = "" if args.no_newline else "\n"` on the final iteration before `print(message, end=end)`
- [ ] The implementation does not build a repeated list or joined output string and does not import `sys`
- [ ] `src/nmg_sdlc_smoke/greet.py` and `src/nmg_sdlc_smoke/__init__.py` are untouched
- [ ] No runtime dependency, new module, or `VERSION`/`CHANGELOG.md` change

**Notes**: Empty `end` still applies only to the final iteration when `--no-newline` is set. Prefix and uppercase already form `message` before the output loop and remain unchanged.

---

## Phase 2: Verification

### T002: Unit tests for AC1 and AC2 only

**File(s)**: `tests/test_cli.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] `main(["--repeat", "2", "--separator", " | ", "Ada"]) == 0` and stdout is exactly `Hello, Ada | Hello, Ada\n` with empty stderr
- [ ] `main(["--repeat", "2", "Ada"]) == 0` and stdout is exactly `Hello, Ada\nHello, Ada\n` with empty stderr
- [ ] Existing `test_cli_prints_greeting` still expects `main(["Ada"]) == 0` and `Hello, Ada\n`
- [ ] Existing uppercase, repeat, prefix, and no-newline tests remain without weakened expectations
- [ ] No new unit tests for missing TEXT, empty TEXT, `--repeat 1` with separator, flag-order, uppercase+separator, prefix+separator, or `--no-newline`+separator
- [ ] `tests/test_greet.py` is untouched
- [ ] `python -m pytest tests/test_cli.py tests/test_greet.py` exits 0

### T003: Add pytest-bdd feature and separator steps for AC1–AC2

**File(s)**: `tests/features/add_nmg_smoke_separator_text_option.feature`, `tests/features/steps/test_separator_steps.py`
**Type**: Create
**Depends**: T002
**Acceptance**:
- [ ] Feature file is the executable Gherkin from `feature.gherkin` without the spec metadata header
- [ ] Scenarios `@SCN001` and `@SCN002` map 1:1 to AC1 and AC2; no further scenarios exist
- [ ] Steps call `nmg_sdlc_smoke.cli.main` in-process with `capsys`; no subprocess or installed-binary dependency
- [ ] `scenarios("../add_nmg_smoke_separator_text_option.feature")` lives only in `test_separator_steps.py`
- [ ] `pytest_plugins = ["test_greeting_steps", "test_repeat_steps", "test_no_newline_steps"]` reuses existing shared steps without redefining them
- [ ] AC1 When-step runs `["--repeat", "2", "--separator", " | ", "Ada"]` and asserts stdout `Hello, Ada | Hello, Ada\n`
- [ ] AC2 When-step runs `["--repeat", "2", "Ada"]` and asserts stdout `Hello, Ada\nHello, Ada\n`
- [ ] Existing feature and step modules are unchanged
- [ ] `python -m pytest tests/features` exits 0

---

## Phase 3: Docs

### T004: Document --separator in README CLI section

**File(s)**: `README.md`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- [ ] Existing `nmg-smoke Ada`, `--uppercase`, `--repeat COUNT`, `--prefix TEXT`, and `--no-newline` CLI examples remain
- [ ] CLI documentation states that `nmg-smoke --repeat 2 --separator ' | ' Ada` writes `Hello, Ada | Hello, Ada` followed by a single newline
- [ ] Library section is unchanged
- [ ] README does not hardcode a VERSION literal
- [ ] `VERSION` and `CHANGELOG.md` are not edited in this task

---

## Dependency Graph

```
T001 ──┬──▶ T002 ──▶ T003
       └──▶ T004
```

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #98 | 2026-09-07 | Initial feature spec |

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
