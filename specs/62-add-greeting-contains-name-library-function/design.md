# Design: Add greeting_contains_name library function

**Issue**: #62
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greeting_contains_name(name: str) -> bool` next to `greet`, `greeting_length`, and `greeting_is_ascii` in `src/nmg_sdlc_smoke/greet.py`. It returns `name in greet(name)` so the result is always the Python bool for whether the current greeting string contains the supplied name. Invalid names propagate `greet`'s `ValueError("name must not be blank")` unwrapped. Export `greeting_contains_name` from `src/nmg_sdlc_smoke/__init__.py` without dropping `greet`, `greeting_is_ascii`, `greeting_length`, or any already-exported names. Do not change `greet`, `greeting_length`, `greeting_is_ascii`, `cli.py`, or the console script. Requirements: `specs/62-add-greeting-contains-name-library-function/requirements.md`. Neighbors: `specs/44-add-greeting-length-library-function/` and `specs/57-add-greeting-is-ascii-library-function/`. Issue #53 (`greeting_bytes`) is not a blocker.

No equivalent containment helper exists. Do not add a new module.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greeting_is_ascii,      │
│                            greeting_length,                │
│                            greeting_contains_name          │
│  greeting_contains_name(name) → bool                       │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  greeting_length(name: str) -> int  (unchanged)            │
│  greeting_is_ascii(name: str) -> bool  (unchanged)         │
│  ValueError("name must not be blank")                      │
│  greeting_contains_name(name: str) -> bool                 │
│    return name in greet(name)                              │
└──────────────────────────────────────────────────────────┘

CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greeting_contains_name.
```

No database, HTTP, or UI. Do not add a new module.

### Data Flow

```
1. Caller invokes greeting_contains_name(name)
2. greeting_contains_name calls greet(name)
3. If greet raises ValueError("name must not be blank"), that exception propagates unwrapped
4. Otherwise return (name in greeting)
5. Examples: greeting_contains_name("Ada") is True because "Ada" in "Hello, Ada"
             greeting_contains_name("Jo") is True because "Jo" in "Hello, Jo"
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greeting_contains_name(name: str) -> bool` | library function | No | whether `greet(name)` contains `name` |

Append `greeting_contains_name` to `nmg_sdlc_smoke.__all__` beside existing public names. Current `src/nmg_sdlc_smoke/__init__.py` is:

```python
from .greet import greet, greeting_is_ascii, greeting_length

__all__ = ["greet", "greeting_is_ascii", "greeting_length"]
```

Change it to:

```python
from .greet import greet, greeting_is_ascii, greeting_length, greeting_contains_name

__all__ = ["greet", "greeting_is_ascii", "greeting_length", "greeting_contains_name"]
```

If `greeting_bytes` is already imported and listed in `__all__` when this issue is implemented, keep that name and append `greeting_contains_name` after the existing names.

`greet` stays `greet(name: str) -> str`. `greeting_length` stays `greeting_length(name: str) -> int`. `greeting_is_ascii` stays `greeting_is_ascii(name: str) -> bool`. `main(argv: list[str] | None = None) -> int` stays. Do not edit `src/nmg_sdlc_smoke/cli.py`.

Implementation in `greet.py` immediately after `greeting_is_ascii` (after `greeting_bytes` if that function already exists). No equivalent containment helper exists:

```python
def greeting_contains_name(name: str) -> bool:
    return name in greet(name)
```

Do not reimplement blank-name checks in `greeting_contains_name`. Do not `return True`. Do not return `"True"` / `"False"` strings. Do not add a needle argument. Do not implement case-insensitive or token-boundary matching.

### Request / Response Schemas

#### greeting_contains_name(name)

**Input:** a name (`str`). Same contract as `greet`.

**Output (success):** Python `bool` equal to `name in greet(name)`. Examples: `greeting_contains_name("Ada") is True`; `greeting_contains_name("Jo") is True`.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `ValueError("name must not be blank")` | blank, whitespace-only, or non-string `name`; raised by `greet`, not wrapped |

#### greet(name), greeting_length(name), greeting_is_ascii(name), and nmg-smoke NAME (unchanged)

**Input / output / errors:** unchanged from `specs/57-add-greeting-is-ascii-library-function/` and the current CLI.

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
| **A: `return name in greet(name)` in `greet.py`** | Reuse greeting and validation | Always matches `greet` membership; one module; no extra validation | Callers import a second symbol | **Selected** |
| **B: `return True`** | Constant because current format always contains the name | Slightly less work | Diverges if greeting format changes; violates AC1/AC2 membership equality | Rejected |
| **C: new `contains.py` module** | Separate file | Isolation | Extra module against structure steering | Rejected |
| **D: CLI containment flag or two-argument needle** | Visible from the shell / extra argument | Discoverable | Out of scope | Rejected |

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
| Library | Unit `tests/test_greet.py` | Ada → `True` and equals `"Ada" in greet("Ada")`; Jo → `True` and equals `"Jo" in greet("Jo")` and not Ada-only; blank/whitespace/non-string `ValueError`; existing `greet` / `greeting_length` / `greeting_is_ascii` tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC4 CLI |
| Feature | pytest-bdd `tests/features/add_greeting_contains_name_library_function.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greeting_length` / `greeting_is_ascii` / `greeting_contains_name` in-process, matching `tests/test_greet.py`. Do not hardcode a VERSION literal. CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_is_ascii_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greeting_contains_name_steps.py` calling `scenarios("../add_greeting_contains_name_library_function.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`, `test_greeting_length_steps.py`, or `test_greeting_is_ascii_steps.py`. Do not edit `pyproject.toml` pytest markers; reuse existing `@SCN001`–`@SCN004` marker names.

Gherkin step texts (executable feature omits spec frontmatter):

- Reuse existing phrases for AC4 and shared Then/Given text: `Given the library is importable`, `Then it returns True`, `Then it raises ValueError with message name must not be blank`, `And that error is the existing greet validation error, not a wrapped or renamed error`, `Given the distribution is installed`, `When greet is called with Ada`, `Then it returns Hello, Ada`, `When nmg-smoke Ada is run`, `Then the process exits 0 and prints Hello, Ada followed by a single newline`, `And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting`.
- Unique When/Then texts that must live only in `test_greeting_contains_name_steps.py`: `When greeting_contains_name is called with Ada`; `And that value equals Ada in greet Ada which is Hello, Ada`; `And the return value is the Python bool True, not the string True`; `When greeting_contains_name is called with Jo`; `And that value equals Jo in greet Jo which is Hello, Jo`; `And the result is not hardcoded to the Ada call only`; `When greeting_contains_name is called with a blank, whitespace-only, or non-string name`.
- The unique invalid-name When must populate `context["errors"]` and `context["greet_errors"]` the same way as `tests/features/steps/test_greeting_is_ascii_steps.py` (values `""`, `" "`, `"\t"`, `"\n"`, `None`, `42`; compare type+message; `__cause__` and `__context__` are `None`) so the reused Then steps still work if they bind, and so a local copy of those Then steps can assert the same contract.
- Unique Then for Ada membership: `assert greet("Ada") == "Hello, Ada"` and `assert context["result"] is True` and `assert context["result"] == ("Ada" in greet("Ada"))`.
- Unique Then for bool identity: `assert context["result"] is True` and `assert context["result"] != "True"`.
- Unique Then for Jo membership: `assert greet("Jo") == "Hello, Jo"` and `assert context["result"] is True` and `assert context["result"] == ("Jo" in greet("Jo"))`.
- Unique Then not hardcoded to Ada: `assert context["result"] == ("Jo" in greet("Jo"))` and `assert "Ada" not in greet("Jo")` and `assert greeting_contains_name("Ada") is True`.
- Unique Then True: if a local `Then it returns True` is required because pytest-bdd does not bind the existing ascii step, `assert context["result"] is True` (identity, not string compare).

If pytest-bdd rejects duplicate step definitions across modules, keep the unique When/Then texts in `test_greeting_contains_name_steps.py` and omit duplicate copies of already-defined Given/Then/When phrases so the existing definitions bind. Do not change those existing step implementations.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hardcoding `return True` instead of `name in greet(name)` | Med | High | Implement as `return name in greet(name)`; AC1/AC2 assert equality with membership |
| Returning `"True"` / `"False"` strings | Med | High | Unit and BDD asserts use `is True` |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greeting_contains_name` |
| CLI, `greet`, `greeting_length`, or `greeting_is_ascii` edits | Low | High | Leave `cli.py` and those function bodies/signatures untouched |
| Treating Ada as the only exercised name | Med | High | AC2 uses `Jo` and asserts `"Ada" not in greet("Jo")` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #62 | 2026-09-01 | Initial feature spec |
