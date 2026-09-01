# Design: Add greeting_length library function

**Issue**: #44
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greeting_length(name: str) -> int` next to `greet` in `src/nmg_sdlc_smoke/greet.py`. It returns `len(greet(name))` so the count is always the Python `len()` of the current greeting string (Unicode code points), including the `Hello, ` prefix. Invalid names propagate `greet`'s `ValueError("name must not be blank")` unwrapped. Export `greeting_length` from `src/nmg_sdlc_smoke/__init__.py`. Do not change `greet`, `cli.py`, or the console script. Requirements: `specs/44-add-greeting-length-library-function/requirements.md`.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greeting_length         │
│  greeting_length(name) → int                               │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  ValueError("name must not be blank")                      │
│  greeting_length(name: str) -> int                         │
│    return len(greet(name))                                 │
└──────────────────────────────────────────────────────────┘

CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greeting_length.
```

No database, HTTP, or UI. Do not add a new module.

### Data Flow

```
1. Caller invokes greeting_length(name)
2. greeting_length calls greet(name)
3. If greet raises ValueError("name must not be blank"), that exception propagates unwrapped
4. Otherwise return len(of that greeting string)
5. Examples: greeting_length("Ada") == 10 because greet("Ada") == "Hello, Ada"
             greeting_length("Jo") == 9 because greet("Jo") == "Hello, Jo"
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greeting_length(name: str) -> int` | library function | No | Character count of `greet(name)` |

Append `greeting_length` to `nmg_sdlc_smoke.__all__` beside existing public names. `greet` signature stays `greet(name: str) -> str`. `main(argv: list[str] | None = None) -> int` stays.

Implementation in `greet.py` (no equivalent length helper exists today):

```python
def greeting_length(name: str) -> int:
    return len(greet(name))
```

Place it in the same module after `greet`. Do not reimplement blank-name checks in `greeting_length`.

### Request / Response Schemas

#### greeting_length(name)

**Input:** a name (`str`). Same contract as `greet`.

**Output (success):** `int` equal to `len(greet(name))`. Examples: `greeting_length("Ada") == 10`; `greeting_length("Jo") == 9`.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `ValueError("name must not be blank")` | blank, whitespace-only, or non-string `name`; raised by `greet`, not wrapped |

#### greet(name) and nmg-smoke NAME (unchanged)

**Input / output / errors:** unchanged from `specs/35-convert-smoke-repository-to-a-python-sdlc-host/`.

---

## Database / Storage Changes

None. No database.

---

## State Management

None. Pure function. No persistent state.

---

## UI Components

None. Library only.

---

## Alternatives Considered

| Option | Description | Pros | Cons | Decision |
|--------|-------------|------|------|----------|
| **A: `return len(greet(name))` in `greet.py`** | Reuse greeting and validation | Always matches `greet`; one module; no extra validation | Callers import a second symbol | **Selected** |
| **B: count `len(name)` plus a constant prefix** | Avoid calling `greet` | Slightly less work | Diverges if greeting format changes; fails AC1/AC2 coupling | Rejected |
| **C: new `length.py` module** | Separate file | Isolation | Extra module against structure steering | Rejected |
| **D: CLI length flag** | Visible from the shell | Discoverable | Out of scope | Rejected |
| **E: UTF-8 byte count** | `len(greet(name).encode())` | Useful for some encodings | Issue requires Python `len()` of the string | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Reuse `greet`; do not wrap `ValueError`
- [x] **Data Sanitization**: Names are not interpolated beyond `Hello, {name}` inside `greet`
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
| Library | Unit `tests/test_greet.py` | Ada → 10; Jo → 9; blank/whitespace/non-string `ValueError`; existing `greet` tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC4 CLI |
| Feature | pytest-bdd `tests/features/add_greeting_length_library_function.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greeting_length` in-process, matching `tests/test_greet.py`. Do not hardcode a VERSION literal. CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greeting_length_steps.py` calling `scenarios("../add_greeting_length_library_function.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`. Do not edit `pyproject.toml` pytest markers; reuse existing `@SCN001`–`@SCN004` marker names.

Existing step texts in `tests/features/steps/test_greeting_steps.py` that must not be redefined: `When nmg-smoke Ada is run` and `Then the process exits 0 and prints Hello, Ada followed by a single newline`. Implement new unique steps only in `test_greeting_length_steps.py`.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Counting `len(name)` instead of `len(greet(name))` | Med | High | Implement as `return len(greet(name))`; AC1/AC2 assert 10 and 9 |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greeting_length` |
| CLI or `greet` edits | Low | High | Leave `cli.py` and the `greet` body/signature untouched |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #44 | 2026-09-01 | Initial feature spec |
