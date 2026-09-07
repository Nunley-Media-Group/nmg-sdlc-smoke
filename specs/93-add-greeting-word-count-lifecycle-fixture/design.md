# Design: Greeting word-count lifecycle fixture

**Issue**: #93
**Date**: 2026-09-06
**Status**: Approved
**Author**: NMG

## Behavior

Implement a pure typed greeting_word_count(name: str) -> int in src/nmg_sdlc_smoke/greet.py using len(greet(name).split()). Export it in src/nmg_sdlc_smoke/__init__.py consistently with neighboring helpers. Calling greet preserves validation and existing output; no new validation policy, dependencies, CLI flag, or infrastructure is needed. Whitespace splitting uses Python str.split() semantics.

## Verification

Extend tests/test_greet.py for ordinary/multiword names and invalid input; add one independent pytest-bdd feature and step module under tests/features/ using existing conventions. Verify the exported helper rather than implementation text. Add a README import/example. Run python -m pytest, python -m pytest tests/features, and python -m ruff check . in an isolated environment. Normal delivery owns VERSION, CHANGELOG.md, and the verification report.

AC3 is proved by an independent BDD scenario executing the README library example and by running the required verification commands outside pytest. Tests do not recursively launch pytest or Ruff. T003's implementation boundary provides version/changelog and truthful verification evidence; exact-head PR merge and issue closure remain owned by the controller's later delivery step, not this implement worker.

## Scope and progress boundary

This fixture exists solely to test nmg-sdlc #369. An unrelated smoke failure is reported without repair. Do not weaken assertions or fix unrelated application code. A retry requires a concrete changed plugin fix or hypothesis; unchanged/no-progress failure ends the experiment. Follow the current candidate controller through exact-head merge and issue closure; no fabricated handoffs or manual success markers.
