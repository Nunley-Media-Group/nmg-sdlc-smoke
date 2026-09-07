# Requirements: Exact greeting suffix delivery fixture

**Issue**: #96
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

## Feature
Add an optional --suffix TEXT to nmg-smoke as the minimal fresh consumer-delivery fixture for Nunley-Media-Group/nmg-sdlc#372. This issue exists only to exercise the reviewed plugin candidate through its normal issue/spec/implementation/review/verification/exact-head delivery pipeline. The plugin's isolated recovery regressions prove dispatch-once/no-replay; this fresh fixture proves unchanged real consumer delivery and publication gates.

## Current State
The thin argparse CLI supports uppercase, repeat, prefix and no-newline. It has no suffix option. No library change or dependency is needed.

## Acceptance Criteria
### AC1: Append exact suffix to each completed greeting
**Given** a valid name and --suffix TEXT
**When** the CLI renders a greeting, including --uppercase, --prefix, --repeat or --no-newline combinations
**Then** it appends TEXT verbatim after each rendered greeting, without uppercasing or stripping the suffix, while preserving existing repetition and newline semantics.

### AC2: Preserve existing default and error behavior
**Given** --suffix is omitted or empty, or the name is invalid
**When** the CLI runs
**Then** omitted/empty suffix preserves existing successful output and invalid names still exit 1 without stdout greeting or suffix; --help documents --suffix TEXT.

## Scope
Only CLI parsing/rendering, focused CLI/BDD regressions, one README example, and normal version/changelog delivery artifacts. Standard-library only; reuse the existing CLI and test patterns.

## Experiment Contract
Plugin issue #372 hypothesis: the reviewed candidate preserves real normal delivery while its separate isolated tests prove bare recovery safety. Pass requires this fresh issue's controller-recorded pre-merge head and new linked PR to match GitHub MERGED state with the issue CLOSED, as collected by the configured plugin smoke provider. A spec-only PR or old merged issue is not proof. Run one configured exercise; further attempts require a concrete changed in-scope plugin fix/hypothesis. Stop unchanged or two-attempt no-progress failures. Do not repair unrelated smoke backlog or expand this fixture.

## Out of Scope
Library changes, plugin runtime copied into this repo, unrelated open issues, altered steering/gates, new frameworks or compatibility paths.

## Change History

| Issue | Date | Summary |
|---|---|---|
| #96 | 2026-09-07 | Approved minimal fresh delivery fixture required to verify nmg-sdlc #372; not independent smoke backlog work |
