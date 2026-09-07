# Design: Add nmg-smoke --brackets flag

**Issue**: #100
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG

## Overview

Implement the opt-in CLI-only behavior in requirements.md. This disposable fixture preserves the existing pure greeting library and thin argparse adapter; no reusable library API is added.

## Architecture and Data Flow

In src/nmg_sdlc_smoke/cli.py, retain the current order: greet(name), optional uppercase of the greeting, literal prefix prepend. If --brackets is enabled, wrap that composed message once in literal '[' and ']'. Then use the existing repeat loop and final-newline selection unchanged. Existing brackets, whitespace, and embedded newlines inside the composed contents are neither escaped nor rewritten by the wrapping step.

## Interface Changes

Add the long-only boolean --brackets option with no value and an omitted/false default. Existing positional-name validation, repeat-count validation, error status, and stderr behavior remain unchanged. No changes to src/nmg_sdlc_smoke/greet.py or package exports are required.

## Alternatives Considered

Wrapping before prefix composition would leave the prefix outside the brackets and violate AC1. Wrapping the whole repeated output would bracket the batch rather than each greeting. A library helper or configurable delimiter would add out-of-scope behavior. Compose once in the CLI before its existing output loop.

## Security and Performance

No shell execution, escaping layer, external services, storage, or runtime dependencies are introduced. Preserve current validation. When enabled, build the wrapped message once rather than once per repetition; omission does no wrapping work.

## Testing Strategy

Use exactly two pytest-bdd scenarios under tests/features/, corresponding 1:1 to AC1 and AC2. Each scenario checks exact stdout, exit 0, and empty stderr for its two commands. AC1 proves transformation order, literal nested brackets, per-greeting repetition, default LF, and --no-newline composition. AC2 proves byte-identical default and composed output without the flag. Reuse existing console-script invocation and capture patterns under tests/features/steps/; preserve existing invalid-input coverage in tests/test_cli.py.

The delivery owner runs python -m pytest, python -m pytest tests/features, and python -m ruff check ., plus actual console-script smoke commands from AC1 and AC2. No implementation or execution occurs during spec publication.

## Risks and Mitigations

The relevant regression risks are bracketing the wrong transformation stage, uppercasing the prefix, escaping existing brackets, or changing final LF behavior. Exact composed-output assertions cover these risks. No open product questions remain under the accepted fixture context.

## Steering Alignment

Follow steering/manifest.json and its project product, tech, and structure snippets: Python 3.12+, src layout, pure library, thin CLI, zero runtime dependencies, and exact BDD acceptance coverage. Storage, UI components, migrations, and persistent state are not applicable.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #100 | 2026-09-07 | Initial feature spec |
