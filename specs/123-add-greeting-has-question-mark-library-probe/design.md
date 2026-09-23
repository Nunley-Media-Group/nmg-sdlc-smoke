# Design: Greeting question-mark library probe

**Issue**: #123
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## Behavior

Add `greeting_has_question_mark(name: str) -> bool` to `src/nmg_sdlc_smoke/greet.py` as a pure query over `greet(name)`. Export it in `src/nmg_sdlc_smoke/__init__.py` with neighboring helpers. Reusing `greet` preserves existing blank/non-string validation. No CLI or dependency change.

## Verification

Extend `tests/test_greet.py` for the public export and add independent BDD scenarios under `tests/features/` for each AC. Use current pytest-bdd conventions. Run `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .`; record outcomes in a truthful verification report. Normal delivery owns VERSION, CHANGELOG, PR exact-head merge and issue closure.

## Experiment boundary

The installed nmg-sdlc 3.24.4 must produce invocation-bound new PR/head/merge and closed issue evidence for this fresh issue. Status discovery, prior PRs, synthetic handoffs or an unmerged PR do not pass. Stop on unchanged/no-progress or unrelated smoke-project failures rather than expanding scope.
