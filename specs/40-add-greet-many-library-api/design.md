# Design: Add greet_many library API

**Issue**: #40
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greet_many(names: Iterable[str]) -> list[str]` next to `greet` in `src/nmg_sdlc_smoke/greet.py`. It maps the existing `greet` contract across an iterable and returns a list in input order. A bare `str` is rejected with `TypeError("names must not be a str")` before iteration so `"Ada"` cannot become per-character greetings. Empty iterables return `[]`. The first invalid name lets `greet`'s `ValueError("name must not be blank")` propagate unwrapped. Export `greet_many` from `src/nmg_sdlc_smoke/__init__.py`. Do not change `greet`, `cli.py`, or the console script. Requirements: `specs/40-add-greet-many-library-api/requirements.md`.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greet_many              │
│  greet_many(names) → list[str]                             │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  ValueError("name must not be blank")                      │
└──────────────────────────────────────────────────────────┘

CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greet_many.
```

No database, HTTP, or UI. Do not add a new module.

### Data Flow

```
1. Caller invokes greet_many(names)
2. If isinstance(names, str): raise TypeError("names must not be a str")
3. Otherwise iterate names in order
4. For each element, call greet(name) and append the result to a list
5. If greet raises ValueError, that exception propagates; later names are not greeted
6. If the iterable is empty, return []
7. Non-iterable names such as None or int fail with TypeError from the `for` loop;
   do not catch or rewrite that TypeError
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greet_many(names: Iterable[str]) -> list[str]` | library function | No | Batch `greet` in input order |

Add `greet_many` to `nmg_sdlc_smoke.__all__` beside `greet`. `greet` signature stays `greet(name: str) -> str`. `main(argv: list[str] | None = None) -> int` stays.

Implementation in `greet.py` (no equivalent batch helper exists today):

```python
from collections.abc import Iterable

def greet_many(names: Iterable[str]) -> list[str]:
    if isinstance(names, str):
        raise TypeError("names must not be a str")
    return [greet(name) for name in names]
```

### Request / Response Schemas

#### greet_many(names)

**Input:** an iterable of names (list, tuple, or generator). Not a bare `str`.

**Output (success):** `list[str]` in input order. Examples: `greet_many(["Ada", "Bob"]) == ["Hello, Ada", "Hello, Bob"]`; `greet_many(["Ada", "Ada"]) == ["Hello, Ada", "Hello, Ada"]`; `greet_many([]) == []`; `greet_many(("Ada",)) == ["Hello, Ada"]`; `greet_many(n for n in ["Ada"]) == ["Hello, Ada"]`.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `TypeError("names must not be a str")` | `names` is a `str` |
| `ValueError("name must not be blank")` | first invalid element (blank, whitespace-only, or non-string); raised by `greet`, not wrapped |
| `TypeError` from iterator protocol | `names` is not iterable (`None`, `int`); no dedicated message |

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
| **A: map existing `greet` in `greet.py`** | `isinstance(names, str)` then list comprehension | Reuses validation; one module; matches `__all__` | Callers must import a second symbol | **Selected** |
| **B: new `batch.py` module** | Separate file | Isolation | Extra module against structure steering | Rejected |
| **C: CLI multi-name args** | `nmg-smoke Ada Bob` | Visible from the shell | Out of scope | Rejected |
| **D: return a tuple or iterator** | Lazy map | Avoids materializing | Issue requires a list | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Reuse `greet`; reject bare `str` before iteration
- [x] **Data Sanitization**: Names are not interpolated beyond `Hello, {name}`
- [x] **Sensitive Data**: None

---

## Performance Considerations

- [x] **Caching**: None
- [x] **Pagination**: None
- [x] **Lazy Loading**: Eager `list` as required
- [x] **Indexing**: None

---

## Testing Strategy

| Layer | Type | Coverage |
|-------|------|----------|
| Library | Unit `tests/test_greet.py` | ordered names; duplicates; empty list/tuple/generator; first invalid; bare `str`; existing `greet` tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC5 CLI |
| Feature | pytest-bdd `tests/features/add_greet_many_library_api.feature` | AC1–AC5 as `@SCN001`–`@SCN005` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greet_many` in-process, matching `tests/test_greet.py`. Do not hardcode `3.15.0`. CLI assertions in AC5 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greet_many_steps.py` calling `scenarios("../add_greet_many_library_api.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`. Do not edit `pyproject.toml` pytest markers; `@SCN001`–`@SCN005` are already registered.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| `str` is iterable of characters | High | High | `isinstance(names, str)` before the `for` loop |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greet_many` |
| Optional `name` / CLI batch | Low | High | Leave `cli.py` and `parser.add_argument("name")` untouched |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #40 | 2026-08-31 | Initial feature spec |
