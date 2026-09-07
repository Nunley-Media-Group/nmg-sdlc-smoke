# Implementation Verification: Greeting word-count lifecycle fixture

**Issue**: #93
**Date**: 2026-09-06
**Status**: Passed

## Implemented scope

- Public pure `greeting_word_count(name)` returns `len(greet(name).split())`.
- Unit boundaries cover ordinary and multiword names, mixed Unicode whitespace, blank/whitespace-only input, and non-string input.
- Independent BDD scenarios exercise public counts, existing validation and CLI output, and the README library example.
- VERSION is 3.31.0; CHANGELOG preserves released history.

## Evidence

Checks ran in an isolated `.venv` with Python 3.14.6 after editable installation via `.venv/bin/python -m pip install -e '.[dev]'`.

| Command | Result |
|---|---|
| Direct exported-helper smoke | Passed: Ada=2, Ada Lovelace=3, unchanged greet output, invalid input ValueError |
| `.venv/bin/python -m pytest tests/test_greet.py tests/features/steps/test_word_count_steps.py` | 78 passed |
| `.venv/bin/python -m pytest` | 192 passed, 2 skipped, 116 warnings; exit 0 |
| `.venv/bin/python -m pytest tests/features` | 70 passed, 2 skipped, 116 warnings; exit 0 |
| `.venv/bin/python -m ruff check .` | All checks passed; exit 0 |

The two skips are in the existing live-smoke-362-B scenarios; this implementation added no skips or disabled checks. Warnings originate in the installed Gherkin dependency's positional maxsplit argument. No unrelated application repairs were made.

The initial documentation scenario passed pytest but triggered Ruff S102 for `exec`; repaired by executing the example with the isolated Python interpreter in a subprocess. Focused pytest and Ruff then passed. Initial inline smoke invocations had quoting syntax errors; corrected invocation passed without changing application behavior.

## Simplification and delivery boundary

Reviewed the changed helper, export, tests, and documentation for redundant logic. No additional abstraction or behavior-preserving simplification was warranted. Final checks above ran after that review. No throwaway scripts were added.

AC3's verification commands run outside pytest rather than recursively from BDD. The independent documentation scenario verifies the README example in a fresh interpreter.

This report records implementation verification only. Commit/push and upstream equality are enforced before the implement handoff. PR review, exact-head merge, and issue closure belong to subsequent controller steps and are not claimed here. This fixture does not establish cancellation or loop-safety results for nmg-sdlc #369.
