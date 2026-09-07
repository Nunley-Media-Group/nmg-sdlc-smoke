# Design: Exact greeting suffix delivery fixture

**Issue**: #96
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

## Overview
Add one argparse --suffix TEXT string option with an empty default in src/nmg_sdlc_smoke/cli.py. Reuse the existing greeting, uppercase and prefix pipeline, then append the exact suffix before the repeat loop. No new library API or helper module is required.

## Observable Contract
- nmg-smoke --suffix '!' Ada prints Hello, Ada! followed by LF.
- nmg-smoke --uppercase --prefix 'ok: ' --suffix ' done' --repeat 2 --no-newline Ada prints exactly two rendered lines separated by LF, each containing 'ok: HELLO, ADA done', with no trailing LF.
- Empty/omitted suffix is identical to current behavior.
- Blank/whitespace names exit 1 with no stdout, including when suffix is nonempty.
- Existing argparse help exposes --suffix TEXT.

## Architecture and Scope
Keep library pure and CLI thin as registered in steering/manifest.json and project snippets. Modify only existing CLI, focused tests/BDD, README and normal release artifacts. Use standard library only and existing test invocation patterns. No unrelated behavior cleanup.

## Verification
Each AC maps one-to-one to an independent pytest-bdd scenario. Supplement only genuinely distinct CLI boundaries where useful; assert consumer stdout/exit behavior, not source text. Run an actual installed CLI smoke, python -m pytest, python -m pytest tests/features, and python -m ruff check . in an isolated environment. Review/fix/verify/deliver stay with their owning stages.

The parent nmg-sdlc #372 provider must observe a fresh linked closing PR, its exact pre-merge head, MERGED state and CLOSED issue. This fixture proves normal consumer delivery, not bare checkpoint recovery by itself. Do not claim the latter without the plugin's separate isolated proof. Preserve any failure and stop unchanged/no-progress attempts rather than create another fixture.

## Change History

| Issue | Date | Summary |
|---|---|---|
| #96 | 2026-09-07 | Approved minimal fresh delivery fixture required to verify nmg-sdlc #372; not independent smoke backlog work |
