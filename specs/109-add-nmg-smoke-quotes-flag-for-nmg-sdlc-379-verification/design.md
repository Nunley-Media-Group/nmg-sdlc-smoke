# Design: Add nmg-smoke --quotes flag for nmg-sdlc #379 verification

**Issue**: #109
**Date**: 2026-09-13
**Status**: Approved
**Author**: NMG

## Overview

Extend the existing argparse CLI with one long-only boolean `--quotes` option. Keep `greet` pure and the CLI adapter thin. After the current uppercase, prefix, parentheses, and braces transformations, wrap the completed message once with literal double quotes when enabled. The existing repeat loop then prints that message with unchanged newline semantics.

This package is solely the single registered final-verification fixture for Nunley-Media-Group/nmg-sdlc#379. Publication is spec-only; implementation and delivery occur only if the registered provider later executes the issue.

## Observable Contract

- `nmg-smoke --quotes --uppercase --prefix 'ok: ' --parentheses --braces Ada` writes exactly `"{(ok: HELLO, ADA)}"\n`, exits 0, and writes no stderr.
- `nmg-smoke Ada` remains exactly `Hello, Ada\n`, exits 0, and writes no stderr.
- `--quotes` has no short alias and does not escape or otherwise rewrite message contents.
- Existing name validation, repeat behavior, final-newline behavior, and library API remain unchanged.

## Architecture and Data Flow

1. argparse parses existing options, the new `--quotes` boolean, and the required name.
2. `greet(args.name)` runs through the existing validation path.
3. Existing transformations run in their current order: uppercase, prefix, parentheses, braces.
4. When `args.quotes` is true, the completed message becomes `f'"{message}"'`.
5. The existing repeat loop and newline selection print the result unchanged.

No new module, helper abstraction, runtime dependency, storage, network, UI, or library API is needed.

## Verification

Map AC1 and AC2 one-to-one to `@SCN001` and `@SCN002`. Add focused consumer-observable CLI assertions and pytest-bdd coverage following existing in-process `main([...])` and `capsys` patterns. Run the actual CLI smoke, `python -m pytest`, `python -m pytest tests/features`, and `python -m ruff check .` during implementation verification.

Delivery retains normal ownership of the 3.x VERSION bump and CHANGELOG entry. README documents the new flag. `pyproject.toml` remains unchanged and continues reading VERSION dynamically.

## Alternatives Considered

- A value-taking quote option adds unnecessary surface and ambiguity; rejected.
- A library-level formatting helper violates the pure greeting-library boundary; rejected.
- Wrapping before parentheses or braces produces a different composition contract; rejected.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #109 | 2026-09-13 | Initial feature design for the single nmg-sdlc #379 verification fixture |
