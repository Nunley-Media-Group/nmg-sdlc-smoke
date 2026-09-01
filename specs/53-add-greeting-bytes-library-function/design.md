# Design: Add greeting_bytes library function

**Issue**: #53
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greeting_bytes(name: str) -> int` next to `greet` and `greeting_length` in `src/nmg_sdlc_smoke/greet.py`. It returns `len(greet(name).encode("utf-8"))` so the count is always the UTF-8 byte length of the current greeting string, including the `Hello, ` prefix. Invalid names propagate `greet`'s `ValueError("name must not be blank")` unwrapped. Export `greeting_bytes` from `src/nmg_sdlc_smoke/__init__.py` without dropping `greet` or `greeting_length`. Do not change `greet`, `greeting_length`, `cli.py`, or the console script. Requirements: `specs/53-add-greeting-bytes-library-function/requirements.md`. Neighbor: `specs/44-add-greeting-length-library-function/`.

No equivalent byte-count helper exists. Do not add a new module.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greeting_length,        │
│                            greeting_bytes                  │
│  greeting_bytes(name) → int                                │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  greeting_length(name: str) -> int  (unchanged)            │
│  ValueError("name must not be blank")                      │
│  greeting_bytes(name: str) -> int                          │
│    return len(greet(name).encode("utf-8"))                 │
└──────────────────────────────────────────────────────────┘

CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greeting_bytes.
```

No database, HTTP, or UI. Do not add a new module.

### Data Flow

```
1. Caller invokes greeting_bytes(name)
2. greeting_bytes calls greet(name)
3. If greet raises ValueError("name must not be blank"), that exception propagates unwrapped
4. Otherwise return len(greeting.encode("utf-8"))
5. Examples: greeting_bytes("Ada") == 10 because greet("Ada") == "Hello, Ada" (ASCII)
             greeting_bytes("É") == 9 because "É" is two UTF-8 bytes; greeting_length("É") == 8
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greeting_bytes(name: str) -> int` | library function | No | UTF-8 byte length of `greet(name)` |

Append `greeting_bytes` to `nmg_sdlc_smoke.__all__` beside existing public names. Current `src/nmg_sdlc_smoke/__init__.py` is:

```python
from .greet import greet, greeting_length

__all__ = ["greet", "greeting_length"]
```

Change it to:

```python
from .greet import greet, greeting_length, greeting_bytes

__all__ = ["greet", "greeting_length", "greeting_bytes"]
```

`greet` stays `greet(name: str) -> str`. `greeting_length` stays `greeting_length(name: str) -> int`. `main(argv: list[str] | None = None) -> int` stays. Do not edit `src/nmg_sdlc_smoke/cli.py`.

Implementation in `greet.py` immediately after `greeting_length` (no equivalent byte helper exists):

```python
def greeting_bytes(name: str) -> int:
    return len(greet(name).encode("utf-8"))
```

Do not reimplement blank-name checks in `greeting_bytes`. Do not use `len(name)`, `len(greet(name))`, or `.encode()` without `"utf-8"`.

### Request / Response Schemas

#### greeting_bytes(name)

**Input:** a name (`str`). Same contract as `greet`.

**Output (success):** `int` equal to `len(greet(name).encode("utf-8"))`. Examples: `greeting_bytes("Ada") == 10`; `greeting_bytes("É") == 9`.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `ValueError("name must not be blank")` | blank, whitespace-only, or non-string `name`; raised by `greet`, not wrapped |

#### greet(name), greeting_length(name), and nmg-smoke NAME (unchanged)

**Input / output / errors:** unchanged from `specs/44-add-greeting-length-library-function/` and the current CLI.

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
| **A: `return len(greet(name).encode("utf-8"))` in `greet.py`** | Reuse greeting and validation | Always matches `greet` UTF-8 bytes; one module; no extra validation | Callers import a second symbol | **Selected** |
| **B: `return greeting_length(name)` or `len(greet(name))`** | Reuse character count | Simple | Fails AC2 (`É` is 9 bytes, 8 characters) | Rejected |
| **C: count `len(name.encode("utf-8"))` plus a constant prefix** | Avoid calling `greet` | Slightly less work | Diverges if greeting format changes; fails AC1/AC2 coupling | Rejected |
| **D: new `bytes.py` module** | Separate file | Isolation | Extra module against structure steering | Rejected |
| **E: CLI bytes flag** | Visible from the shell | Discoverable | Out of scope | Rejected |

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
| Library | Unit `tests/test_greet.py` | Ada → 10 UTF-8 bytes; É → 9 UTF-8 bytes and not `greeting_length("É")` (8); blank/whitespace/non-string `ValueError`; existing `greet` / `greeting_length` tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC4 CLI |
| Feature | pytest-bdd `tests/features/add_greeting_bytes_library_function.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greeting_length` / `greeting_bytes` in-process, matching `tests/test_greet.py`. Do not hardcode a VERSION literal. CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_length_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greeting_bytes_steps.py` calling `scenarios("../add_greeting_bytes_library_function.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py` or `test_greeting_length_steps.py`. Do not edit `pyproject.toml` pytest markers; reuse existing `@SCN001`–`@SCN004` marker names.

Gherkin step texts (executable feature omits spec frontmatter):

- Reuse existing phrases for AC4 and shared Then/Given text: `Given the library is importable`, `Then it returns 10`, `Then it returns 9`, `And the result is not hardcoded to the Ada count`, `Then it raises ValueError with message name must not be blank`, `And that error is the existing greet validation error, not a wrapped or renamed error`, `Given the distribution is installed`, `When greet is called with Ada`, `Then it returns Hello, Ada`, `When nmg-smoke Ada is run`, `Then the process exits 0 and prints Hello, Ada followed by a single newline`, `And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting`.
- Unique When/Then texts that must live only in `test_greeting_bytes_steps.py`: `When greeting_bytes is called with Ada`; `And that value equals the UTF-8 byte length of greet Ada which is Hello, Ada`; `When greeting_bytes is called with É`; `And that value equals the UTF-8 byte length of greet É which is Hello, É`; `And that value is not equal to greeting_length of É which is 8`; `When greeting_bytes is called with a blank, whitespace-only, or non-string name`.
- The unique invalid-name When must populate `context["errors"]` and `context["greet_errors"]` the same way as `tests/features/steps/test_greeting_length_steps.py` (values `""`, `" "`, `"\t"`, `"\n"`, `None`, `42`; compare type+message; `__cause__` and `__context__` are `None`) so the reused Then steps still work if they bind, and so a local copy of those Then steps can assert the same contract.
- Unique Then for Ada bytes: `assert greet("Ada") == "Hello, Ada"` and `assert context["result"] == len(greet("Ada").encode("utf-8"))`.
- Unique Then for É bytes: `assert greet("É") == "Hello, É"` and `assert context["result"] == len(greet("É").encode("utf-8"))`.
- Unique Then vs character count: `assert greeting_length("É") == 8` and `assert context["result"] != greeting_length("É")`.

If pytest-bdd rejects duplicate step definitions across modules, keep the unique When/Then texts in `test_greeting_bytes_steps.py` and omit duplicate copies of already-defined Given/Then/When phrases so the existing definitions bind. Do not change those existing step implementations.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Counting `len(greet(name))` instead of UTF-8 bytes | Med | High | Implement as `return len(greet(name).encode("utf-8"))`; AC2 asserts 9 vs `greeting_length("É")` 8 |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greeting_bytes` |
| CLI, `greet`, or `greeting_length` edits | Low | High | Leave `cli.py` and those function bodies/signatures untouched |
| Hardcoding Ada's 10 for every name | Med | High | AC2 uses `É` → 9 and asserts not equal to Ada's count |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #53 | 2026-09-01 | Initial feature spec |
