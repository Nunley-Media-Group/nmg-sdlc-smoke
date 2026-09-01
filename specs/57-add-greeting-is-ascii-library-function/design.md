# Design: Add greeting_is_ascii library function

**Issue**: #57
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greeting_is_ascii(name: str) -> bool` next to `greet` and `greeting_length` in `src/nmg_sdlc_smoke/greet.py`. It returns `greet(name).isascii()` so the result is always the Python bool for whether the current greeting string is ASCII, including the `Hello, ` prefix. Invalid names propagate `greet`'s `ValueError("name must not be blank")` unwrapped. Export `greeting_is_ascii` from `src/nmg_sdlc_smoke/__init__.py` without dropping `greet`, `greeting_length`, or any already-exported names. Do not change `greet`, `greeting_length`, `cli.py`, or the console script. Requirements: `specs/57-add-greeting-is-ascii-library-function/requirements.md`. Neighbor: `specs/44-add-greeting-length-library-function/`. Issue #53 (`greeting_bytes`) is not a blocker.

No equivalent ASCII helper exists. Do not add a new module.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greeting_length,        │
│                            greeting_is_ascii               │
│  greeting_is_ascii(name) → bool                            │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  greeting_length(name: str) -> int  (unchanged)            │
│  ValueError("name must not be blank")                      │
│  greeting_is_ascii(name: str) -> bool                      │
│    return greet(name).isascii()                            │
└──────────────────────────────────────────────────────────┘

CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greeting_is_ascii.
```

No database, HTTP, or UI. Do not add a new module.

### Data Flow

```
1. Caller invokes greeting_is_ascii(name)
2. greeting_is_ascii calls greet(name)
3. If greet raises ValueError("name must not be blank"), that exception propagates unwrapped
4. Otherwise return greeting.isascii()
5. Examples: greeting_is_ascii("Ada") is True because greet("Ada") == "Hello, Ada"
             greeting_is_ascii("É") is False because greet("É") == "Hello, É"
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greeting_is_ascii(name: str) -> bool` | library function | No | whether `greet(name)` is ASCII |

Append `greeting_is_ascii` to `nmg_sdlc_smoke.__all__` beside existing public names. Current `src/nmg_sdlc_smoke/__init__.py` is:

```python
from .greet import greet, greeting_length

__all__ = ["greet", "greeting_length"]
```

Change it to:

```python
from .greet import greet, greeting_length, greeting_is_ascii

__all__ = ["greet", "greeting_length", "greeting_is_ascii"]
```

If `greeting_bytes` is already imported and listed in `__all__` when this issue is implemented, keep that name and append `greeting_is_ascii` after the existing names.

`greet` stays `greet(name: str) -> str`. `greeting_length` stays `greeting_length(name: str) -> int`. `main(argv: list[str] | None = None) -> int` stays. Do not edit `src/nmg_sdlc_smoke/cli.py`.

Implementation in `greet.py` immediately after `greeting_length` (after `greeting_bytes` if that function already exists). No equivalent ASCII helper exists:

```python
def greeting_is_ascii(name: str) -> bool:
    return greet(name).isascii()
```

Do not reimplement blank-name checks in `greeting_is_ascii`. Do not call `name.isascii()`. Do not return `"True"` / `"False"` strings.

### Request / Response Schemas

#### greeting_is_ascii(name)

**Input:** a name (`str`). Same contract as `greet`.

**Output (success):** Python `bool` equal to `greet(name).isascii()`. Examples: `greeting_is_ascii("Ada") is True`; `greeting_is_ascii("É") is False`.

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
| **A: `return greet(name).isascii()` in `greet.py`** | Reuse greeting and validation | Always matches `greet` ASCII-ness; one module; no extra validation | Callers import a second symbol | **Selected** |
| **B: `return name.isascii()`** | Skip prefix | Slightly less work | Out of scope; diverges if greeting format gains non-ASCII text | Rejected |
| **C: new `ascii.py` module** | Separate file | Isolation | Extra module against structure steering | Rejected |
| **D: CLI ASCII flag** | Visible from the shell | Discoverable | Out of scope | Rejected |

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
| Library | Unit `tests/test_greet.py` | Ada → `True`; É → `False` and not Ada's result; blank/whitespace/non-string `ValueError`; existing `greet` / `greeting_length` tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC4 CLI |
| Feature | pytest-bdd `tests/features/add_greeting_is_ascii_library_function.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greeting_length` / `greeting_is_ascii` in-process, matching `tests/test_greet.py`. Do not hardcode a VERSION literal. CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_length_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greeting_is_ascii_steps.py` calling `scenarios("../add_greeting_is_ascii_library_function.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py` or `test_greeting_length_steps.py`. Do not edit `pyproject.toml` pytest markers; reuse existing `@SCN001`–`@SCN004` marker names.

Gherkin step texts (executable feature omits spec frontmatter):

- Reuse existing phrases for AC4 and shared Then/Given text: `Given the library is importable`, `Then it raises ValueError with message name must not be blank`, `And that error is the existing greet validation error, not a wrapped or renamed error`, `Given the distribution is installed`, `When greet is called with Ada`, `Then it returns Hello, Ada`, `When nmg-smoke Ada is run`, `Then the process exits 0 and prints Hello, Ada followed by a single newline`, `And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting`.
- Unique When/Then texts that must live only in `test_greeting_is_ascii_steps.py`: `When greeting_is_ascii is called with Ada`; `Then it returns True`; `And that value equals greet Ada isascii which is Hello, Ada`; `When greeting_is_ascii is called with É`; `Then it returns False`; `And that value equals greet É isascii which is Hello, É`; `And the result is not hardcoded to the Ada result`; `When greeting_is_ascii is called with a blank, whitespace-only, or non-string name`.
- The unique invalid-name When must populate `context["errors"]` and `context["greet_errors"]` the same way as `tests/features/steps/test_greeting_length_steps.py` (values `""`, `" "`, `"\t"`, `"\n"`, `None`, `42`; compare type+message; `__cause__` and `__context__` are `None`) so the reused Then steps still work if they bind, and so a local copy of those Then steps can assert the same contract.
- Unique Then for Ada ASCII: `assert greet("Ada") == "Hello, Ada"` and `assert context["result"] is True` and `assert context["result"] == greet("Ada").isascii()`.
- Unique Then for É ASCII: `assert greet("É") == "Hello, É"` and `assert context["result"] is False` and `assert context["result"] == greet("É").isascii()`.
- Unique Then not hardcoded: `assert context["result"] is not True` and `assert context["result"] != greeting_is_ascii("Ada")`.
- Unique Then True/False: `assert context["result"] is True` / `assert context["result"] is False` (identity, not string compare).

If pytest-bdd rejects duplicate step definitions across modules, keep the unique When/Then texts in `test_greeting_is_ascii_steps.py` and omit duplicate copies of already-defined Given/Then/When phrases so the existing definitions bind. Do not change those existing step implementations.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Checking `name.isascii()` instead of `greet(name).isascii()` | Med | High | Implement as `return greet(name).isascii()` |
| Returning `"True"` / `"False"` strings | Med | High | Unit and BDD asserts use `is True` / `is False` |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greeting_is_ascii` |
| CLI, `greet`, or `greeting_length` edits | Low | High | Leave `cli.py` and those function bodies/signatures untouched |
| Hardcoding Ada's `True` for every name | Med | High | AC2 uses `É` → `False` and asserts not equal to Ada's result |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #57 | 2026-09-01 | Initial feature spec |
