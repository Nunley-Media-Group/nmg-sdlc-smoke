# Design: Add nmg-smoke --swapcase flag

**Issue**: #191
**Date**: 2026-09-30
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/188-add-nmg-smoke-lowercase-flag/

## Overview

Add one long-only boolean `--swapcase` option to the existing argparse mutually exclusive `case` group in `src/nmg_sdlc_smoke/cli.py`, registered after `--lowercase`. Combining it with `--uppercase` or `--lowercase` becomes an argparse usage error (exit 2) with no custom validation. Apply `message.swapcase()` as a third branch of the existing casing step, immediately after `greet(args.name)` and before prefix, wrappers, and the repeat/newline loop. `greet` and the library API stay unchanged; no new module or dependency.

## Architecture

1. `main()` keeps `case = parser.add_mutually_exclusive_group()` with `case.add_argument("--uppercase", action="store_true")` and `case.add_argument("--lowercase", action="store_true")`, then adds `case.add_argument("--swapcase", action="store_true")` directly after `--lowercase`. All other arguments keep their current registration and order.
2. `greet(args.name)` runs through the existing validation path; blank names still exit 1 via `parser.exit(1, ...)` before any casing.
3. The casing step becomes:
   - `if args.uppercase: message = message.upper()`
   - `elif args.lowercase: message = message.lower()`
   - `elif args.swapcase: message = message.swapcase()`
4. Prefix, parentheses, braces, quotes, and the repeat/newline loop run unchanged on the cased message.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg-smoke --swapcase NAME` | valid name | stdout `str.swapcase()` of `Hello, <name>` + LF, exit 0 | `str.swapcase()` applied to `greet(NAME)` |
| `nmg-smoke --swapcase` with other formatting flags | valid name plus `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, `--no-newline` | composed output, exit 0 | swapcase precedes prefix and wrappers; prefix text is kept as supplied |
| `nmg-smoke --swapcase --uppercase NAME` / `--swapcase --lowercase NAME` (either order) | two case flags | stderr argparse usage plus `argument --X: not allowed with argument --Y`, empty stdout, exit 2 | mutually exclusive `case` group |
| `nmg-smoke --swapcase " "` | blank name | stderr `nmg-smoke: error: name must not be blank`, empty stdout, exit 1 | existing validation unchanged |
| `nmg-smoke --help` | none | usage shows `[--uppercase \| --lowercase \| --swapcase]`, options list `--swapcase`, exit 0 | argparse help |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Add `--swapcase` to the existing argparse mutually exclusive `case` group | Selected | Standard-library exit-2 usage error with no custom validation code |
| Last-flag-wins or precedence rule | Rejected | Silent ambiguity; issue requires exit 2 |
| Library-level swapcase helper | Rejected | Keeps `greet` pure and the CLI adapter thin |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #191 | 2026-09-30 | Initial feature design |
