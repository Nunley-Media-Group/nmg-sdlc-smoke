# Design: Add nmg-smoke --casefold flag

**Issue**: #197
**Date**: 2026-10-06
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/194-add-nmg-smoke-titlecase-flag/

## Overview

Add one long-only boolean `--casefold` option to the existing argparse mutually exclusive `case` group in `src/nmg_sdlc_smoke/cli.py`, registered after `--titlecase`. Combining it with `--uppercase`, `--lowercase`, `--swapcase`, or `--titlecase` becomes an argparse usage error (exit 2) with no custom validation. Apply `message.casefold()` as a fifth branch of the existing casing step, immediately after `greet(args.name)` and before prefix, wrappers, and the repeat/newline loop. `greet`, `greeting_casefold`, and the library API stay unchanged; no new module or dependency.

## Architecture

1. `main()` keeps `case = parser.add_mutually_exclusive_group()` with `--uppercase`, `--lowercase`, `--swapcase`, and `--titlecase`, then adds `case.add_argument("--casefold", action="store_true")` directly after `--titlecase`. All other arguments keep their current registration and order.
2. `greet(args.name)` runs through the existing validation path; blank names still exit 1 via `parser.exit(1, ...)` before any casing.
3. The casing step becomes:
   - `if args.uppercase: message = message.upper()`
   - `elif args.lowercase: message = message.lower()`
   - `elif args.swapcase: message = message.swapcase()`
   - `elif args.titlecase: message = message.title()`
   - `elif args.casefold: message = message.casefold()`
4. Prefix, parentheses, braces, quotes, and the repeat/newline loop run unchanged on the cased message.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg-smoke --casefold NAME` | valid name | stdout `str.casefold()` of `Hello, <name>` + LF, exit 0 | `str.casefold()` applied to `greet(NAME)` |
| `nmg-smoke --casefold` with other formatting flags | valid name plus `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, `--no-newline` | composed output, exit 0 | casefolding precedes prefix and wrappers; prefix text is kept as supplied |
| `nmg-smoke --casefold` with `--uppercase`, `--lowercase`, `--swapcase`, or `--titlecase` (either order) | two case flags | stderr argparse usage plus `argument --X: not allowed with argument --Y`, empty stdout, exit 2 | mutually exclusive `case` group |
| `nmg-smoke --casefold " "` | blank name | stderr `nmg-smoke: error: name must not be blank`, empty stdout, exit 1 | existing validation unchanged |
| `nmg-smoke --help` | none | usage shows `[--uppercase \| --lowercase \| --swapcase \| --titlecase \| --casefold]`, options list `--casefold`, exit 0 | argparse help |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| Add `--casefold` to the existing argparse mutually exclusive `case` group and call `str.casefold()` inline | Selected | Matches the four existing case flags; standard-library exit-2 usage error with no custom validation code |
| Call `greeting_casefold(args.name)` from the CLI | Rejected | Would bypass the single `greet(args.name)` validation/greeting path and add a second rendering branch |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #197 | 2026-10-06 | Initial feature design |
