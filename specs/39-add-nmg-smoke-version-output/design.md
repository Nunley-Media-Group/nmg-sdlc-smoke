# Design: Add nmg-smoke --version output

**Issue**: #39
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG
---

## Overview

Extend the existing `nmg-smoke` argparse CLI so `--version` prints the installed distribution version and exits 0 without a name. The version string comes from `importlib.metadata.version("nmg-sdlc-smoke-python")` at parse time, not from the `VERSION` file and not from a new library export. `greet` and the greeting path stay unchanged. Requirements: `specs/39-add-nmg-smoke-version-output/requirements.md`.

The CLI already uses argparse in `src/nmg_sdlc_smoke/cli.py`. Add argparse `action="version"` with the metadata version as the `version=` value. That action prints the supplied string plus a newline to stdout and exits 0, including when the required positional `name` is absent, and including when a name is also present. Do not add `-V`. Do not change `parser.add_argument("name")` to optional.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                      │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main        │
│  argparse: required name XOR --version action              │
└───────────────────────────┬──────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌──────────────────────────┐   ┌──────────────────────────┐
│ Business Logic           │   │ Stdlib metadata          │
│ nmg_sdlc_smoke.greet     │   │ importlib.metadata       │
│ greet(name: str) -> str  │   │ version("nmg-sdlc-smoke- │
│ (unchanged)              │   │ python")                 │
└──────────────────────────┘   └──────────────────────────┘
```

No database, HTTP, or UI. Library package surface stays `__all__ = ["greet"]`.

### Data Flow

```
1. Caller invokes nmg-smoke [args]
2. main() builds ArgumentParser(prog="nmg-smoke")
3. Parser has required positional name and --version action="version"
   with version=importlib.metadata.version("nmg-sdlc-smoke-python")
4. If --version is present: argparse prints that bare version plus LF to stdout
   and exits 0 (SystemExit). greet is not called.
5. If --version is absent and name is missing: argparse exits non-zero with
   usage on stderr and no greeting (existing behavior).
6. If name is present: greet as today; print Hello, {name} plus LF; return 0.
   Blank name still parser.exit(1) with no stdout greeting.
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg-smoke --version` | console flag | No | Print installed distribution version |

No new Python functions. Do not add `version` to `nmg_sdlc_smoke.__init__`. `main(argv: list[str] | None = None) -> int` signature stays.

### Request / Response Schemas

#### nmg-smoke --version

**Input:** argv contains `--version`; name may be absent or present.

**Output (success):** stdout UTF-8 exactly `{importlib.metadata.version("nmg-sdlc-smoke-python")}\n`; process exit 0. No `nmg-smoke` prefix, no distribution-name prefix, no extra blank line.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `importlib.metadata.PackageNotFoundError` | Distribution is not installed; not a supported runtime. Tests and CLI assume `python -m pip install -e ".[dev]"` (or an equivalent install). Do not catch this and fall back to `VERSION`. |

#### nmg-smoke NAME (unchanged)

**Input:** argv positional `name` without `--version`

**Output (success):** stdout `Hello, Ada\n` for `Ada`; `main` returns 0

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| exit `1` | `ValueError` from `greet`; stdout has no greeting |
| argparse non-zero | missing positional when `--version` is absent; usage on stderr; no greeting |

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
| **A: argparse `action="version"`** | Add `--version` with `version=importlib.metadata.version("nmg-sdlc-smoke-python")` | Matches existing argparse CLI; name stays required; `--version` exits before greeting | Uses `SystemExit` like other argparse actions | **Selected** |
| **B: optional name + custom `--version` branch** | `nargs="?"` then `if args.version` | Explicit Python branch | Changes missing-name argparse error path (AC3) | Rejected |
| **C: read root `VERSION` file** | Open `VERSION` from disk | Works without install | Issue requires installed package metadata; breaks library-must-not-depend-on-repo-layout | Rejected |
| **D: public `nmg_sdlc_smoke.version`** | Library export | Convenient for importers | Out of scope | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Greeting validation unchanged; `--version` takes no value
- [x] **Data Sanitization**: Version string is package metadata, not user input
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
| CLI | Unit `tests/test_cli.py` | `--version`; `--version` with name; `Ada` greeting; no-args non-zero |
| Feature | pytest-bdd `tests/features/add_nmg_smoke_version_output.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `main([...])` in-process with `capsys`, matching `tests/test_cli.py`. Version action raises `SystemExit(0)`; assert `exit_info.value.code == 0` and `captured.out == f"{importlib.metadata.version('nmg-sdlc-smoke-python')}\n"` and `captured.err == ""`. Do not hardcode `3.15.0`. Greeting tests must still see `main(["Ada"]) == 0` without `SystemExit`. No-args: `main([])` raises `SystemExit` with non-zero code and empty stdout.

Register the new feature with a new steps module `tests/features/steps/test_version_steps.py` calling `scenarios("../add_nmg_smoke_version_output.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`. Do not edit `pyproject.toml` pytest markers; `@SCN001`–`@SCN004` are already registered.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| argparse `version=` includes prog name | Low | High | Pass the bare metadata string only; never `%(prog)s` |
| Name made optional to allow `--version` | Low | High | Keep required `name`; argparse version action exits first |
| Tests assert `VERSION` file bytes | Med | Med | Assert `importlib.metadata.version("nmg-sdlc-smoke-python")` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #39 | 2026-08-31 | Initial feature spec |
