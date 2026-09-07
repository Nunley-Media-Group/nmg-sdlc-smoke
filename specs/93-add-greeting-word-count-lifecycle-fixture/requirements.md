# Requirements: Add greeting_word_count lifecycle fixture

**Issue**: #93
**Date**: 2026-09-06
**Status**: Approved
**Author**: NMG

## User Story

As an nmg-sdlc maintainer, I want a minimal deterministic Python change to exercise nmg-sdlc #369 through the actual approved-spec -> execute -> exact-head merge lifecycle. This is a test fixture for the plugin, not authorization to repair the smoke application backlog.

## Acceptance Criteria

### AC1: Count greeting words
Given a valid name, when greeting_word_count(name) is imported from nmg_sdlc_smoke and called, then it returns the number of whitespace-separated words in greet(name): Ada returns 2 and Ada Lovelace returns 3.

### AC2: Preserve validation and existing behavior
Given blank, whitespace-only, or non-string input, when greeting_word_count is called, then it raises the same ValueError as greet. Existing greet, helpers, and CLI output remain unchanged.

### AC3: Independent observable proof
Given the fixture implementation, when the existing pytest, pytest-bdd, and Ruff commands run, then they pass with focused boundary coverage and a README example for the new import.

## Scope and experiment stop
Only add this small helper, its public export, behavior tests/BDD scenario, README example, and normal workflow-owned spec/verification/version/changelog artifacts. No unrelated smoke repairs, new infrastructure, CLI changes, or disabled checks. An unrelated failure stops the experiment with evidence. Any rerun must name a concrete changed nmg-sdlc fix or hypothesis; never loop unchanged. The test objective is nmg-sdlc #369 lifecycle progression/owned worker cleanup; this issue does not itself claim that cancellation or loop safety passed.


## Change History

| Issue | Date | Summary |
|---|---|---|
| #93 | 2026-09-06 | Approved minimal fixture for nmg-sdlc #369 live lifecycle verification |
