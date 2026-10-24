# Root Cause Analysis: Ignore the nmg-sdlc v4 runtime directory .nmg-sdlc/

**Issue**: #219
**Date**: 2026-10-24
**Status**: Approved
**Author**: NMG

## Root Cause

nmg-sdlc 4.0 moved its runtime state from `.omp/sdlc/` to `.nmg-sdlc/`, and `/sdlc-upgrade-project`'s `nmg-sdlc-ignore` migration swaps the host ignore rule to match. This repository was never upgraded, so its `.gitignore` still ignores only `.omp/sdlc/`.

## Affected Code

| File | Role |
|------|------|
| `.gitignore` | Carries the v3 runtime rule |

## Fix Strategy

Replace the `.omp/sdlc/` line in place with `.nmg-sdlc/`. The legacy `.omp/sdlc/` directory is not present, so the migration drops the legacy rule.
