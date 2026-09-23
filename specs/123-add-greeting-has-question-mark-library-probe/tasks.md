# Tasks: Greeting question-mark library probe

**Issue**: #123
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

### T001: Implement pure exported query
**File(s)**: src/nmg_sdlc_smoke/greet.py, src/nmg_sdlc_smoke/__init__.py
**Type**: Modify
**Acceptance**: AC1–AC3 observable return and existing validation behavior; no CLI changes.

### T002: Verify independent outcomes
**File(s)**: tests/test_greet.py, tests/features/, README.md
**Type**: Modify and Create
**Acceptance**: AC1–AC3 unit/BDD cases, public example and existing pytest/Ruff checks.

### T003: Publish real lifecycle evidence
**File(s)**: VERSION, CHANGELOG.md, specs/123-add-greeting-has-question-mark-library-probe/verification-report.md
**Type**: Modify and Create
**Acceptance**: Exact-head merged PR and issue closure only after genuine registered verification and normal delivery.

Behavior for src/nmg_sdlc_smoke/: preserve `greet` validation and expose the query.
Behavior for tests/: assert public API outcomes and each approved scenario.
