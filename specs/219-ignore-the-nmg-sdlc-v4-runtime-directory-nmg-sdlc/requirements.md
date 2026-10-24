# Defect Report: Ignore the nmg-sdlc v4 runtime directory .nmg-sdlc/

**Issue**: #219
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Reproduction

1. With nmg-sdlc 4.x, run any workflow in this repository. It writes `.nmg-sdlc/prompt-provenance/*.json`.
2. `git status --porcelain` reports `?? .nmg-sdlc/`, and start-issue and spec publication stop with `dirty_tree`.

## Expected vs Actual

| | Description |
|---|-------------|
| **Expected** | `.nmg-sdlc/` is ignored, as nmg-sdlc's runtime-ignore contract requires of a host. |
| **Actual** | `.gitignore` still carries only the v3 rule `.omp/sdlc/`. |

## Acceptance Criteria

### AC1: The v4 runtime directory is ignored

**Given** this repository's `.gitignore`
**When** nmg-sdlc 4.x writes files under `.nmg-sdlc/`
**Then** `git status --porcelain` lists nothing for them, and the legacy `.omp/sdlc/` rule has been replaced in place by `.nmg-sdlc/`, with every other rule preserved

## Functional Requirements

| ID | Requirement | Priority |
|----|-------------|----------|
| FR1 | `.gitignore` replaces `.omp/sdlc/` in place with `.nmg-sdlc/` (the nmg-sdlc `nmg-sdlc-ignore` migration) | Must |
