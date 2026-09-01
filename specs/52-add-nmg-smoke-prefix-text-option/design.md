# Design: Add nmg-smoke --prefix TEXT option

**Issue**: #52
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Extend the existing `nmg-smoke` argparse CLI so `--prefix TEXT` prepends TEXT exactly as supplied to each successful printed greeting line. `greet(name: str) -> str` stays `Hello, {name}` and still raises `ValueError("name must not be blank")`. `--prefix` is long-only. The positional `name` stays required. Neighboring delivered CLI options `--uppercase` (#43) and `--repeat COUNT` (#45) stay; prefix is applied after uppercase and before the repeat print loop. Requirements: `specs/52-add-nmg-smoke-prefix-text-option/requirements.md`.

Live code: `src/nmg_sdlc_smoke/cli.py` already parses `--uppercase`, `--repeat COUNT`, and required `name`; calls `greet`; uppercases the message when flagged; then `print(message)` `args.repeat` times. On `ValueError` it uses `parser.exit(1, f"nmg-smoke: error: {error}\n")`. Add `parser.add_argument("--prefix", default="", metavar="TEXT")` with no short option and no `nargs`. After the existing uppercase transform and before the repeat loop, set `message = args.prefix + message`. Do not add `-p`. Do not change `greet.py` or `__init__.py`.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                      │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main        │
│  argparse: required name + --uppercase + --repeat COUNT    │
│            + optional --prefix TEXT                        │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ Business Logic                                             │
│ nmg_sdlc_smoke.greet                                       │
│ greet(name: str) -> str  (unchanged)                       │
│ CLI prepends TEXT to the already-transformed greeting      │
└──────────────────────────────────────────────────────────┘
```

No database, HTTP, or UI. Library package surface stays `__all__ = ["greet", "greeting_length"]`; this issue does not add or remove exports.

### Data Flow

```
1. Caller invokes nmg-smoke [args]
2. main() builds ArgumentParser(prog="nmg-smoke")
3. Parser already has --uppercase, --repeat COUNT, required positional name.
   Add --prefix TEXT with default="", metavar="TEXT", dest prefix
4. Missing TEXT (bare --prefix with no following token): argparse SystemExit
   non-zero; usage or error on stderr; no greeting on stdout; greet not called
5. Missing name (including with a valid --prefix TEXT): argparse SystemExit
   non-zero; usage on stderr; no greeting
6. Name present: greet(args.name) as today
7. ValueError → parser.exit(1, "nmg-smoke: error: {error}\n"); stdout has no greeting
8. Success:
   if args.uppercase: message = message.upper()
   message = args.prefix + message
   for _ in range(args.repeat): print(message)
   omit --prefix → one Hello, Ada\n
   --prefix 'OK: ' Ada → OK: Hello, Ada\n
   --prefix 'OK: ' --uppercase Ada → OK: HELLO, ADA\n
   --prefix 'OK: ' --repeat 2 Ada → OK: Hello, Ada\nOK: Hello, Ada\n
   --prefix '' Ada → Hello, Ada\n (same as omit)
```

`--prefix` may appear before or after the positional name (argparse default). TEXT is not a library concern. Do not insert an extra space or separator beyond the supplied TEXT.

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg-smoke --prefix TEXT NAME` | console option | No | Prepend TEXT to each successful printed greeting line |

No new public Python functions. `main(argv: list[str] | None = None) -> int` signature stays. Do not add `prefix` to `nmg_sdlc_smoke.__init__`.

### Request / Response Schemas

#### nmg-smoke --prefix TEXT NAME

**Input:** argv contains `--prefix`, a TEXT token, and positional `name`. Order may be `--prefix OK:  Ada` (argv `["--prefix", "OK: ", "Ada"]`) or `Ada --prefix OK: ` (argv `["Ada", "--prefix", "OK: "]`).

**Output (success):** for TEXT `OK: ` and name `Ada`, stdout UTF-8 exactly `OK: Hello, Ada\n`; `main` returns 0; stderr empty.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| argparse non-zero | `--prefix` with no TEXT token; usage or error on stderr; no greeting on stdout |
| argparse non-zero | `--prefix TEXT` with no name; usage on stderr; no greeting |
| exit `1` | `ValueError` from `greet` (blank/whitespace name) even when `--prefix` TEXT is present; stdout has no greeting; stderr includes `name must not be blank` |

#### nmg-smoke NAME (unchanged)

**Input:** argv positional `name` without `--prefix`

**Output (success):** stdout `Hello, Ada\n` for `Ada`; `main` returns 0

**Errors:** unchanged blank-name `parser.exit(1, ...)` path.

#### greet(name) (unchanged)

**Input:** `name: str`

**Output:** `Hello, Ada` for `"Ada"`

**Errors:** `ValueError("name must not be blank")` for blank, whitespace-only, and non-string names.

---

## Database / Storage Changes

None. No database.

---

## State Management

None. Single invocation. No persistent state.

---

## UI Components

None. CLI only.

---

## Alternatives Considered

| Option | Description | Pros | Cons | Decision |
|--------|-------------|------|------|----------|
| **A: argparse `--prefix` default="" then `prefix + message` after uppercase** | CLI-only prepend; omit and empty TEXT share one path | Leaves library contract intact; TEXT not uppercased | Prefix lives in the adapter | **Selected** |
| **B: `greet(name, prefix="")`** | Library owns the prefix | Reusable | Changes `greet` API; issue forbids it | Rejected |
| **C: short `-p`** | Unix-style short option | Shorter to type | FR5 forbids it | Rejected |
| **D: prepend before uppercase** | Simpler if transform order ignored | One less comment | Would uppercase TEXT; AC7/FR8 forbid it | Rejected |
| **E: `nargs="?"` so bare `--prefix` is allowed** | Missing TEXT would not error | Fewer argparse failures | AC3 requires missing TEXT to fail | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Greeting validation unchanged in `greet`; missing TEXT is argparse; TEXT is concatenated as supplied
- [x] **Data Sanitization**: TEXT is prepended unchanged to the already-validated greeting string
- [x] **Sensitive Data**: None

---

## Performance Considerations

- [x] **Caching**: None
- [x] **Pagination**: None
- [x] **Lazy Loading**: None
- [x] **Indexing**: None

---

## Testing Strategy

| Layer | Type | Coverage |
|-------|------|----------|
| CLI | Unit `tests/test_cli.py` | `--prefix OK:  Ada`; `Ada --prefix OK: `; omit `--prefix`; empty TEXT; missing TEXT; `--prefix` without name; blank name with `--prefix`; `--prefix` with `--uppercase`; `--prefix` with `--repeat 2` |
| Library | Unit `tests/test_greet.py` | Untouched; existing Ada and blank/non-string cases remain the AC4 proof |
| Feature | pytest-bdd `tests/features/add_nmg_smoke_prefix_text_option.feature` | AC1–AC7 as `@SCN001`–`@SCN007` |
| Lint | Ruff | `src` and `tests` |

Keep calling `main([...])` in-process with `capsys`, matching `tests/test_cli.py`. Happy-path `main` still returns `0` (does not raise `SystemExit`). Missing TEXT and missing name raise `SystemExit` with non-zero code and empty stdout. Blank name with `--prefix`: `SystemExit` code `1`, empty stdout, `name must not be blank` on stderr.

Register the new feature with a new steps module `tests/features/steps/test_prefix_steps.py` calling `scenarios("../add_nmg_smoke_prefix_text_option.feature")`. Set `pytest_plugins = ["test_greeting_steps", "test_uppercase_steps", "test_repeat_steps"]` so existing Given/When/Then texts are reused. Do not add a second `scenarios(...)` to `test_greeting_steps.py`. Do not redefine step texts that already exist in `tests/features/steps/test_greeting_steps.py`, `test_uppercase_steps.py`, or `test_repeat_steps.py`. Do not edit `pyproject.toml` pytest markers.

Reuse these existing step texts unchanged:

- `the distribution is installed with its console script`
- `nmg-smoke Ada is run`
- `the process exits 0 and prints Hello, Ada followed by a single newline`
- `stderr is empty`
- `the library is importable`
- `a caller invokes greet with Ada`
- `the function returns exactly Hello, Ada`
- `blank, whitespace-only, and non-string names still raise ValueError with message name must not be blank`
- `a blank or whitespace-only name`
- `the CLI exits non-zero without printing a greeting to stdout`
- `the distribution is installed`
- `the process exits non-zero and does not print a greeting`

New step texts only for prefix-specific When/Then lines. AC3 When-step must invoke `main(["--prefix"])`. AC5 When-step must invoke `main(["--prefix", "OK: ", str(context["blank_name"])])`. AC6 When-step must invoke `main(["--prefix", "OK: "])`. AC7 When-step invokes `main(["--prefix", "OK: ", "--uppercase", "Ada"])`; the following And-step invokes `main(["--prefix", "OK: ", "--repeat", "2", "Ada"])` and asserts stdout `OK: Hello, Ada\nOK: Hello, Ada\n`; the TEXT-not-uppercased And-step asserts the AC7 uppercase stdout starts with `OK: ` not `OK: `.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Extra separator inserted (`prefix + " " + message`) | Med | High | Concatenate `args.prefix + message`; tests use `OK: ` with trailing space |
| Prefix applied before uppercase so TEXT is uppercased | Med | High | Apply prefix after `message.upper()`; AC7 expects `OK: HELLO, ADA` |
| Name made optional so `--prefix` can stand alone | Low | High | Keep required `name`; missing name stays argparse failure |
| Short `-p` added by habit | Low | Med | `add_argument("--prefix", default="", metavar="TEXT")` with no short option |
| `nargs="?"` makes missing TEXT succeed | Med | High | Require TEXT; AC3 covers bare `--prefix` |
| `greet` gains a prefix parameter | Low | High | Do not edit `greet.py` or `__init__.py` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #52 | 2026-09-01 | Initial feature spec |
