# Design: Add nmg-smoke --repeat COUNT option

**Issue**: #45
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Extend the existing `nmg-smoke` argparse CLI so `--repeat COUNT` prints the successful `greet` result exactly COUNT times, one line per greeting. `greet(name: str) -> str` stays `Hello, {name}` and still raises `ValueError("name must not be blank")`. `--repeat` is long-only. COUNT is a positive integer parsed by argparse. The positional `name` stays required. Requirements: `specs/45-add-nmg-smoke-repeat-count-option/requirements.md`.

Live code: `src/nmg_sdlc_smoke/cli.py` parses required `name`, calls `greet`, prints the message plus newline on success, and on `ValueError` uses `parser.exit(1, f"nmg-smoke: error: {error}\n")`. Add `--repeat` with `type=_positive_count`, `default=1`, `metavar="COUNT"`. After a successful `greet`, loop `print(message)` `args.repeat` times. Do not add `-r`. Do not change `greet.py` or `__init__.py`.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                      │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main        │
│  argparse: required name + optional --repeat COUNT         │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ Business Logic                                             │
│ nmg_sdlc_smoke.greet                                       │
│ greet(name: str) -> str  (unchanged)                       │
│ CLI repeats print() of that one string COUNT times         │
└──────────────────────────────────────────────────────────┘
```

No database, HTTP, or UI. Library package surface stays `__all__ = ["greet"]` unless a previously delivered spec already added other exports; this issue does not add or remove exports.

### Data Flow

```
1. Caller invokes nmg-smoke [args]
2. main() builds ArgumentParser(prog="nmg-smoke")
3. Parser has required positional name and --repeat COUNT
   type=_positive_count, default=1, metavar="COUNT"
4. Invalid COUNT (missing, non-integer, 0, negative): argparse SystemExit
   non-zero; usage or error on stderr; no greeting on stdout; greet not called
5. Missing name (including with a valid --repeat COUNT): argparse SystemExit
   non-zero; usage on stderr; no greeting
6. Name present: greet(args.name) as today
7. ValueError → parser.exit(1, "nmg-smoke: error: {error}\n"); stdout has no greeting
8. Success: for _ in range(args.repeat): print(message); return 0
   omit --repeat or --repeat 1 → one Hello, Ada\n
   --repeat 3 → Hello, Ada\nHello, Ada\nHello, Ada\n
```

`--repeat` may appear before or after the positional name (argparse default). COUNT is not a library concern.

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg-smoke --repeat COUNT NAME` | console option | No | Print the existing greeting COUNT times |
| `_positive_count(value: str) -> int` | private argparse type in `cli.py` | No | Parse COUNT; reject non-int and integers less than 1 with `ArgumentTypeError` |

No new public Python functions. `main(argv: list[str] | None = None) -> int` signature stays. Do not add `repeat` or `_positive_count` to `nmg_sdlc_smoke.__init__`.

### Request / Response Schemas

#### nmg-smoke --repeat COUNT NAME

**Input:** argv contains `--repeat`, a COUNT token, and positional `name`. Order may be `--repeat 3 Ada` or `Ada --repeat 3`.

**Output (success):** for COUNT `3` and name `Ada`, stdout UTF-8 exactly `Hello, Ada\nHello, Ada\nHello, Ada\n`; `main` returns 0; stderr empty.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| argparse non-zero | missing COUNT, non-integer COUNT, `0`, negative COUNT; usage or error on stderr; no greeting on stdout |
| argparse non-zero | `--repeat 2` with no name; usage on stderr; no greeting |
| exit `1` | `ValueError` from `greet` (blank/whitespace name) even when `--repeat` is valid; stdout has no greeting; stderr includes `name must not be blank` |

Negative COUNT as a separate argv token (`--repeat`, `-1`, `Ada`) is argparse option-parsing failure. Attached `--repeat=-1` reaches `_positive_count` and raises `ArgumentTypeError`. Both are AC3 failures.

#### nmg-smoke NAME (unchanged)

**Input:** argv positional `name` without `--repeat`

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
| **A: argparse `--repeat` + `_positive_count` + print loop** | CLI-only repeat after successful `greet`; default COUNT 1 | Leaves library contract intact; omit and `--repeat 1` share one path | Repeat lives in the adapter | **Selected** |
| **B: library `repeat_greet` / change `greet`** | Reusable helper | Callers outside CLI | Issue forbids library repeat helper and `greet` changes | Rejected |
| **C: short `-r`** | Unix-style short option | Shorter to type | FR5 forbids it | Rejected |
| **D: `type=int` then reject values less than 1 after parse** | Slightly less code | Same behavior | Custom type fails at the same argparse layer as non-integers | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Greeting validation unchanged in `greet`; COUNT validated by `_positive_count` before `greet`
- [x] **Data Sanitization**: COUNT is an int used only as `range()` bound; greeting string is already validated
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
| CLI | Unit `tests/test_cli.py` | `--repeat 3 Ada`; `Ada --repeat 3`; `--repeat 1 Ada`; `Ada` unchanged; invalid COUNT cases; `--repeat 2` without name; blank name with `--repeat 2` |
| Library | Unit `tests/test_greet.py` | Untouched; existing Ada and blank/non-string cases remain the AC4 proof |
| Feature | pytest-bdd `tests/features/add_nmg_smoke_repeat_count_option.feature` | AC1–AC6 as `@SCN001`–`@SCN006` |
| Lint | Ruff | `src` and `tests` |

Keep calling `main([...])` in-process with `capsys`, matching `tests/test_cli.py`. Happy-path `main` still returns `0` (does not raise `SystemExit`). Invalid COUNT and missing name raise `SystemExit` with non-zero code and empty stdout. Blank name with `--repeat 2`: `SystemExit` code `1`, empty stdout, `name must not be blank` on stderr.

Register the new feature with a new steps module `tests/features/steps/test_repeat_steps.py` calling `scenarios("../add_nmg_smoke_repeat_count_option.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`. Do not redefine step texts that already exist in `tests/features/steps/test_greeting_steps.py`. Do not edit `pyproject.toml` pytest markers.

AC3 step must invoke all four invalid COUNT shapes:

1. `main(["--repeat"])` — missing COUNT
2. `main(["--repeat", "abc", "Ada"])` — non-integer
3. `main(["--repeat", "0", "Ada"])` — zero
4. `main(["--repeat", "-1", "Ada"])` — negative as a separate token (argparse option-like failure)

Each must be non-zero `SystemExit`, empty stdout, nonempty stderr that is not required to contain `name must not be blank`.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `range(0)` silently prints nothing and exits 0 | Med | High | `_positive_count` rejects integers less than 1; tests cover `0` |
| Name made optional so `--repeat` can stand alone | Low | High | Keep required `name`; missing name stays argparse failure |
| Short `-r` added by habit | Low | Med | `add_argument("--repeat", ...)` with no short option |
| `greet` called COUNT times or gains a repeat parameter | Low | High | Call `greet` once; do not edit `greet.py` or `__init__.py` |
| Separate-token `-1` parsed as an option | Med | Low | Treat as argparse failure; also unit-test `--repeat=-1` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #45 | 2026-09-01 | Initial feature spec |
