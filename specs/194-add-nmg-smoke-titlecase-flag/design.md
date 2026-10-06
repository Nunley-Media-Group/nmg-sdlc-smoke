# Design: Add nmg-smoke --titlecase flag

**Issue**: #194
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/191-add-nmg-smoke-swapcase-flag/

## Overview

Add one long-only boolean `--titlecase` option to the existing argparse mutually exclusive `case` group in `src/nmg_sdlc_smoke/cli.py`, registered after `--swapcase`. Combining it with `--uppercase`, `--lowercase`, or `--swapcase` becomes an argparse usage error (exit 2) with no custom validation. Apply `message.title()` as a fourth branch of the existing casing step, immediately after `greet(args.name)` and before prefix, wrappers, and the repeat/newline loop. `greet` and the library API stay unchanged; no new module or dependency.

## Architecture

1. `main()` keeps `case = parser.add_mutually_exclusive_group()` with `--uppercase`, `--lowercase`, and `--swapcase`, then adds `case.add_argument("--titlecase", action="store_true")` directly after `--swapcase`. All other arguments keep their current registration and order.
2. `greet(args.name)` runs through the existing validation path; blank names still exit 1 via `parser.exit(1, ...)` before any casing.
3. The casing step becomes:
   - `if args.uppercase: message = message.upper()`
   - `elif args.lowercase: message = message.lower()`
   - `elif args.swapcase: message = message.swapcase()`
   - `elif args.titlecase: message = message.title()`
4. Prefix, parentheses, braces, quotes, and the repeat/newline loop run unchanged on the cased message.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg-smoke --titlecase NAME` | valid name | stdout `str.title()` of `Hello, <name>` + LF, exit 0 | `str.title()` applied to `greet(NAME)` |
| `nmg-smoke --titlecase` with other formatting flags | valid name plus `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, `--no-newline` | composed output, exit 0 | title-casing precedes prefix and wrappers; prefix text is kept as supplied |
| `nmg-smoke --titlecase` with `--uppercase`, `--lowercase`, or `--swapcase` (either order) | two case flags | stderr argparse usage plus `argument --X: not allowed with argument --Y`, empty stdout, exit 2 | mutually exclusive `case` group |
| `nmg-smoke --titlecase " "` | blank name | stderr `nmg-smoke: error: name must not be blank`, empty stdout, exit 1 | existing validation unchanged |
| `nmg-smoke --help` | none | usage shows `[--uppercase \| --lowercase \| --swapcase \| --titlecase]`, options list `--titlecase`, exit 0 | argparse help |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Add `--titlecase` to the existing argparse mutually exclusive `case` group | Selected | Standard-library exit-2 usage error with no custom validation code |
| Apostrophe-aware title-casing (e.g. `string.capwords`) | Rejected | Issue requires Python `str.title()` semantics, including `O'Neil` |
| Library-level title-case helper | Rejected | Keeps `greet` pure and the CLI adapter thin |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #194 | 2026-10-06 | Initial feature design |
