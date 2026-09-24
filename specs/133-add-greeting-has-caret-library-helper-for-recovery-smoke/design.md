# Design: Add greeting_has_caret library helper for recovery smoke

**Issue**: #133
**Date**: 2026-09-23
**Status**: Approved
**Author**: NMG

## Approach
Add a typed pure helper in `src/nmg_sdlc_smoke/greet.py` that calls `greet(name)` and checks literal `^` membership in the returned text. Export it from `src/nmg_sdlc_smoke/__init__.py` and its `__all__` list. Calling `greet` first preserves its invalid-name `ValueError` without duplicate validation.

Cover the positive, negative, and invalid-name outcomes in `tests/test_greet.py` and three scenarios with matching steps in `tests/features/`. Add a concise public library usage example to `README.md`. No CLI, package, runtime dependency, or other helper changes are needed; delivery-owned `VERSION` and `CHANGELOG.md` remain governed by the normal release stage.

## Verification
Run `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` in the issue checkout. Registered nmg-sdlc verification must additionally prove a new invocation-bound closing PR exact head and issue closure, not infer success from local tests.
