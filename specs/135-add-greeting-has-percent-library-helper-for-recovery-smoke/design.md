# Design: Add greeting_has_percent library helper for recovery smoke

**Issue**: #135
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## Approach
Add a typed pure helper in `src/nmg_sdlc_smoke/greet.py` that calls `greet(name)` and checks literal `%` membership in its completed greeting. Export it from `src/nmg_sdlc_smoke/__init__.py` and `__all__`. Reusing `greet` preserves blank/non-string validation without duplicate policy.

Cover present, absent, and invalid-name outcomes in `tests/test_greet.py` and independent pytest-bdd scenarios under `tests/features/`. Document a public usage example in `README.md`. Do not change CLI behavior or runtime dependencies; delivery-owned `VERSION` and `CHANGELOG.md` remain under the normal release stage.

## Verification
Run `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .`. Registered nmg-sdlc smoke must additionally prove an invocation-bound new closing PR at its observed exact head and issue closure, not infer success from local tests.
