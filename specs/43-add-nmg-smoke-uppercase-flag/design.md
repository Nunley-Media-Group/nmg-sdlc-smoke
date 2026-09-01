# Design: Add nmg-smoke --uppercase flag

**Issue**: #43
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Extend the existing `nmg-smoke` argparse CLI so `--uppercase` uppercases the successful `greet` result before printing. `greet(name: str) -> str` stays `Hello, {name}` and still raises `ValueError("name must not be blank")`. The flag is long-only (`store_true`). The positional `name` stays required. Requirements: `specs/43-add-nmg-smoke-uppercase-flag/requirements.md`.

Live code: `src/nmg_sdlc_smoke/cli.py` parses required `name`, calls `greet`, prints the message plus newline on success, and on `ValueError` uses `parser.exit(1, f"nmg-smoke: error: {error}\n")`. Add `parser.add_argument("--uppercase", action="store_true")` and `print(message.upper() if args.uppercase else message)`. Do not add `-u`. Do not change `greet.py` or `__init__.py`.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                      │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main        │
│  argparse: required name + optional --uppercase            │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ Business Logic                                             │
│ nmg_sdlc_smoke.greet                                       │
│ greet(name: str) -> str  (unchanged)                       │
│ CLI applies str.upper() to the successful greeting only    │
└──────────────────────────────────────────────────────────┘
```

No database, HTTP, or UI. Library package surface stays `__all__ = ["greet"]` unless a previously delivered spec already added other exports; this issue does not add or remove exports.

### Data Flow

```
1. Caller invokes nmg-smoke [args]
2. main() builds ArgumentParser(prog="nmg-smoke")
3. Parser has required positional name and --uppercase action="store_true"
4. If name is missing: argparse exits non-zero with usage on stderr and no greeting
5. If name is present: greet(args.name) as today
6. ValueError → parser.exit(1, "nmg-smoke: error: {error}\n"); stdout has no greeting
7. Success without flag: print(message) → Hello, Ada\n; return 0
8. Success with flag: print(message.upper()) → HELLO, ADA\n; return 0
```

Flag may appear before or after the positional name (argparse default). Uppercase is `str.upper()` on the full greeting string, not a name-only transform.

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg-smoke --uppercase NAME` | console flag | No | Print the existing greeting line in uppercase |

No new Python functions. `main(argv: list[str] | None = None) -> int` signature stays. Do not add `uppercase` to `nmg_sdlc_smoke.__init__`.

### Request / Response Schemas

#### nmg-smoke --uppercase NAME

**Input:** argv contains `--uppercase` and positional `name`. Order may be `--uppercase Ada` or `Ada --uppercase`.

**Output (success):** stdout UTF-8 exactly `HELLO, ADA\n` for name `Ada`; `main` returns 0; stderr empty.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| argparse non-zero | `--uppercase` with no name; usage on stderr; no greeting on stdout |
| exit `1` | `ValueError` from `greet` (blank/whitespace name); stdout has no greeting; stderr includes `name must not be blank` |

#### nmg-smoke NAME (unchanged)

**Input:** argv positional `name` without `--uppercase`

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
| **A: argparse `store_true` + `str.upper()` on greet result** | CLI-only transform after successful `greet` | Leaves library contract intact; flag optional; name stays required | Uppercase lives in the adapter | **Selected** |
| **B: `greet(name, uppercase=False)`** | Library owns the transform | Reusable | Changes `greet` API; issue forbids it | Rejected |
| **C: short `-u`** | Unix-style short flag | Shorter to type | FR7 forbids it | Rejected |
| **D: uppercase only the name portion** | `Hello, ADA` | Preserves greeting prefix case | Issue requires full-line `HELLO, ADA` | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Greeting validation unchanged in `greet`; `--uppercase` takes no value
- [x] **Data Sanitization**: `str.upper()` on the already-validated greeting string
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
| CLI | Unit `tests/test_cli.py` | `--uppercase Ada`; `Ada --uppercase`; `Ada` unchanged; `--uppercase` without name; blank name with flag |
| Library | Unit `tests/test_greet.py` | Untouched; existing Ada and blank/non-string cases remain the AC5 proof |
| Feature | pytest-bdd `tests/features/add_nmg_smoke_uppercase_flag.feature` | AC1–AC5 as `@SCN001`–`@SCN005` |
| Lint | Ruff | `src` and `tests` |

Keep calling `main([...])` in-process with `capsys`, matching `tests/test_cli.py`. Happy-path `main` still returns `0` (does not raise `SystemExit`). Missing name: `main(["--uppercase"])` raises `SystemExit` with non-zero code and empty stdout. Blank name with flag: `SystemExit` code `1`, empty stdout, `name must not be blank` on stderr.

Register the new feature with a new steps module `tests/features/steps/test_uppercase_steps.py` calling `scenarios("../add_nmg_smoke_uppercase_flag.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`. Do not redefine step texts that already exist in `tests/features/steps/test_greeting_steps.py`. Do not edit `pyproject.toml` pytest markers.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Uppercase applied only to the name | Low | High | Transform `greet` output with `str.upper()` |
| Name made optional so the flag can stand alone | Low | High | Keep required `name`; missing name stays argparse failure |
| Short `-u` added by habit | Low | Med | `add_argument("--uppercase", action="store_true")` with no short option |
| `greet` gains an uppercase parameter | Low | High | Do not edit `greet.py` or `__init__.py` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #43 | 2026-09-01 | Initial feature spec |
