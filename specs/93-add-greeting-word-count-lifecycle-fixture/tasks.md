# Tasks: Greeting word-count lifecycle fixture

**Issue**: #93
**Date**: 2026-09-06
**Status**: Approved
**Author**: NMG

### T001: Add the pure public helper
**File(s)**: src/nmg_sdlc_smoke/greet.py, src/nmg_sdlc_smoke/__init__.py
**Type**: Modify
**Acceptance**:
- [ ] AC1/AC2: exported word count yields 2 for Ada, 3 for Ada Lovelace, and preserves greet validation without changing existing behavior.

### T002: Verify the observable fixture
**File(s)**: tests/test_greet.py, tests/features/, README.md
**Type**: Modify and Create
**Acceptance**:
- [ ] AC3: focused unit and pytest-bdd behavior coverage, README example, and the existing pytest and Ruff commands pass.

### T003: Complete normal lifecycle evidence
**File(s)**: VERSION, CHANGELOG.md, specs/93-add-greeting-word-count-lifecycle-fixture/verification-report.md
**Type**: Modify and Create
**Acceptance**:
- [ ] Publish truthful verification, versioned exact-head PR delivery, and issue closure; do not fix unrelated smoke findings.

Behavior for src/nmg_sdlc_smoke/: expose greeting word count while preserving input validation.
Behavior for tests/: prove exported library outcomes and approved BDD scenarios.
