# Design: Add nmg-smoke --lowercase flag

**Issue**: #188
**Date**: 2026-09-27
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/43-add-nmg-smoke-uppercase-flag/

## Overview

Add one long-only boolean `--lowercase` option to the existing argparse CLI in `src/nmg_sdlc_smoke/cli.py`. Move the existing `--uppercase` registration and the new `--lowercase` registration into one argparse mutually exclusive group so combining them is an argparse usage error (exit 2). Apply `message.lower()` in the same branch position as `message.upper()`, immediately after `greet(args.name)` and before prefix, wrappers, and the repeat/newline loop. `greet` and the library API stay unchanged; no new module or dependency.

## Architecture

1. `main()` creates `case = parser.add_mutually_exclusive_group()` in place of the current top-level `parser.add_argument("--uppercase", action="store_true")`, then registers `case.add_argument("--uppercase", action="store_true")` followed by `case.add_argument("--lowercase", action="store_true")`. All other arguments keep their current registration and order.
2. `greet(args.name)` runs through the existing validation path; blank names still exit 1 via `parser.exit(1, ...)` before any casing.
3. The casing step becomes:
   - `if args.uppercase: message = message.upper()`
   - `elif args.lowercase: message = message.lower()`
4. Prefix, parentheses, braces, quotes, and the repeat/newline loop run unchanged on the cased message.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg-smoke --lowercase NAME` | valid name | stdout `hello, <name lowercased>` + LF, exit 0 | `str.lower()` applied to `greet(NAME)` |
| `nmg-smoke --lowercase` with other formatting flags | valid name plus `--prefix`, `--parentheses`, `--braces`, `--quotes`, `--repeat`, `--no-newline` | composed output, exit 0 | lowercase precedes prefix and wrappers; prefix text is kept as supplied |
| `nmg-smoke --uppercase --lowercase NAME` (either order) | both flags | stderr argparse usage plus `argument --X: not allowed with argument --Y`, empty stdout, exit 2 | mutually exclusive group |
| `nmg-smoke --lowercase " "` | blank name | stderr `nmg-smoke: error: name must not be blank`, empty stdout, exit 1 | existing validation unchanged |
| `nmg-smoke --help` | none | usage shows `[--uppercase \| --lowercase]`, options list `--lowercase`, exit 0 | argparse help |

## Alternatives Considered

| Option | Decision | Reason |
|--------|----------|--------|
| argparse mutually exclusive group for `--uppercase`/`--lowercase` | Selected | Standard-library exit-2 usage error with no custom validation code |
| Last-flag-wins or precedence rule | Rejected | Silent ambiguity; issue requires exit 2 |
| `str.casefold()` | Rejected | Changes `ß` to `ss`; issue requires `str.lower()` semantics |
| Library-level lowercase helper | Rejected | Keeps `greet` pure and the CLI adapter thin |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #188 | 2026-09-27 | Initial feature design |
