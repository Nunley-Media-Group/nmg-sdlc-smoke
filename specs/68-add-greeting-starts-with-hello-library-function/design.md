# Design: Add greeting_starts_with_hello library function

**Issue**: #68
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greeting_starts_with_hello(name: str) -> bool` next to `greet`, `greeting_length`, and `greeting_is_ascii` in `src/nmg_sdlc_smoke/greet.py`. It returns `greet(name).startswith("Hello, ")` so the result is always the Python bool for whether the current greeting string starts with the seven-character literal `Hello, ` (capital H, comma, trailing space). Invalid names propagate `greet`'s `ValueError("name must not be blank")` unwrapped. Export `greeting_starts_with_hello` from `src/nmg_sdlc_smoke/__init__.py` without dropping `greet`, `greeting_is_ascii`, `greeting_length`, or any already-exported names. Do not change `greet`, `greeting_length`, `greeting_is_ascii`, `cli.py`, or the console script. Requirements: `specs/68-add-greeting-starts-with-hello-library-function/requirements.md`. Neighbors: `specs/44-add-greeting-length-library-function/`, `specs/57-add-greeting-is-ascii-library-function/`, `specs/62-add-greeting-contains-name-library-function/`. Issue #53 (`greeting_bytes`) is an approved spec, not a blocker.

No equivalent prefix helper exists. Do not add a new module.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greeting_is_ascii,      │
│                            greeting_length,                │
│                            greeting_starts_with_hello      │
│  greeting_starts_with_hello(name) → bool                   │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  greeting_length(name: str) -> int  (unchanged)            │
│  greeting_is_ascii(name: str) -> bool  (unchanged)         │
│  ValueError("name must not be blank")                      │
│  greeting_starts_with_hello(name: str) -> bool             │
│    return greet(name).startswith("Hello, ")                │
└──────────────────────────────────────────────────────────┘

CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greeting_starts_with_hello.
```

No database, HTTP, or UI. Do not add a new module.

### Data Flow

```
1. Caller invokes greeting_starts_with_hello(name)
2. greeting_starts_with_hello calls greet(name)
3. If greet raises ValueError("name must not be blank"), that exception propagates unwrapped
4. Otherwise return greeting.startswith("Hello, ")
5. Examples: greeting_starts_with_hello("Ada") is True because greet("Ada") == "Hello, Ada"
             greeting_starts_with_hello("Jo") is True because greet("Jo") == "Hello, Jo"
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greeting_starts_with_hello(name: str) -> bool` | library function | No | whether `greet(name)` starts with `Hello, ` |

Append `greeting_starts_with_hello` to `nmg_sdlc_smoke.__all__` beside existing public names. Current `src/nmg_sdlc_smoke/__init__.py` is:

```python
from .greet import greet, greeting_is_ascii, greeting_length

__all__ = ["greet", "greeting_is_ascii", "greeting_length"]
```

Change it to:

```python
from .greet import greet, greeting_is_ascii, greeting_length, greeting_starts_with_hello

__all__ = ["greet", "greeting_is_ascii", "greeting_length", "greeting_starts_with_hello"]
```

If `greeting_bytes` or `greeting_contains_name` is already imported and listed in `__all__` when this issue is implemented, keep those names and append `greeting_starts_with_hello` after the existing names.

`greet` stays `greet(name: str) -> str`. `greeting_length` stays `greeting_length(name: str) -> int`. `greeting_is_ascii` stays `greeting_is_ascii(name: str) -> bool`. `main(argv: list[str] | None = None) -> int` stays. Do not edit `src/nmg_sdlc_smoke/cli.py`.

Implementation in `greet.py` immediately after `greeting_is_ascii` (after `greeting_contains_name` or `greeting_bytes` if that function already exists). No equivalent prefix helper exists:

```python
def greeting_starts_with_hello(name: str) -> bool:
    return greet(name).startswith("Hello, ")
```

Do not reimplement blank-name checks in `greeting_starts_with_hello`. Do not `return True`. Do not call `name.startswith("Hello, ")`. Do not return `"True"` / `"False"` strings. Do not implement case-insensitive or substring matching.

### Request / Response Schemas

#### greeting_starts_with_hello(name)

**Input:** a name (`str`). Same contract as `greet`.

**Output (success):** Python `bool` equal to `greet(name).startswith("Hello, ")`. Examples: `greeting_starts_with_hello("Ada") is True`; `greeting_starts_with_hello("Jo") is True`.

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
| **A: `return greet(name).startswith("Hello, ")` in `greet.py`** | Reuse greeting and validation | Always matches live `greet` prefix; one module; no extra validation | Callers import a second symbol | **Selected** |
| **B: `return True`** | Constant because current format always starts with `Hello, ` | Slightly less work | Diverges if greeting format changes; violates AC1/AC2 prefix equality | Rejected |
| **C: `return name.startswith("Hello, ")`** | Skip `greet` | Slightly less work | Out of scope; ignores greeting contract and validation | Rejected |
| **D: new `prefix.py` module or CLI flag** | Separate file / shell visibility | Isolation / discoverable | Extra module or CLI change against structure steering / out of scope | Rejected |

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
| Library | Unit `tests/test_greet.py` | Ada → `True` and equals `greet("Ada").startswith("Hello, ")`; Jo → `True` and equals `greet("Jo").startswith("Hello, ")` and not Ada-only; blank/whitespace/non-string `ValueError`; existing `greet` / `greeting_length` / `greeting_is_ascii` tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC4 CLI |
| Feature | pytest-bdd `tests/features/add_greeting_starts_with_hello_library_function.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greeting_length` / `greeting_is_ascii` / `greeting_starts_with_hello` in-process, matching `tests/test_greet.py`. Do not hardcode a VERSION literal. CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_is_ascii_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greeting_starts_with_hello_steps.py` calling `scenarios("../add_greeting_starts_with_hello_library_function.feature")`. Do not add a second `scenarios(...)` to `test_greeting_steps.py`, `test_greeting_length_steps.py`, or `test_greeting_is_ascii_steps.py`. Do not edit `pyproject.toml` pytest markers; reuse existing `@SCN001`–`@SCN004` marker names.

Gherkin step texts (executable feature omits spec frontmatter):

- Reuse existing phrases for AC4 and shared Then/Given text: `Given the library is importable`, `Then it returns True`, `Then it raises ValueError with message name must not be blank`, `And that error is the existing greet validation error, not a wrapped or renamed error`, `Given the distribution is installed`, `When greet is called with Ada`, `Then it returns Hello, Ada`, `When nmg-smoke Ada is run`, `Then the process exits 0 and prints Hello, Ada followed by a single newline`, `And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting`.
- Unique When/Then texts that must live only in `test_greeting_starts_with_hello_steps.py`: `When greeting_starts_with_hello is called with Ada`; `And that value equals greet Ada startswith Hello comma space which is Hello, Ada`; `And the return value is the Python bool True, not the string True`; `When greeting_starts_with_hello is called with Jo`; `And that value equals greet Jo startswith Hello comma space which is Hello, Jo`; `And the result is not hardcoded to the Ada call only`; `When greeting_starts_with_hello is called with a blank, whitespace-only, or non-string name`.
- The unique invalid-name When must populate `context["errors"]` and `context["greet_errors"]` the same way as `tests/features/steps/test_greeting_is_ascii_steps.py` (values `""`, `" "`, `"\t"`, `"\n"`, `None`, `42`; compare type+message; `__cause__` and `__context__` are `None`) so the reused Then steps still work if they bind, and so a local copy of those Then steps can assert the same contract.
- Unique Then for Ada prefix: `assert greet("Ada") == "Hello, Ada"` and `assert context["result"] is True` and `assert context["result"] == greet("Ada").startswith("Hello, ")`.
- Unique Then for bool identity: `assert context["result"] is True` and `assert context["result"] != "True"`.
- Unique Then for Jo prefix: `assert greet("Jo") == "Hello, Jo"` and `assert context["result"] is True` and `assert context["result"] == greet("Jo").startswith("Hello, ")`.
- Unique Then not hardcoded to Ada: `assert context["result"] == greet("Jo").startswith("Hello, ")` and `assert greet("Jo") != greet("Ada")` and `assert greeting_starts_with_hello("Ada") is True`.
- Unique Then True: if a local `Then it returns True` is required because pytest-bdd does not bind the existing ascii step, `assert context["result"] is True` (identity, not string compare).

If pytest-bdd rejects duplicate step definitions across modules, keep the unique When/Then texts in `test_greeting_starts_with_hello_steps.py` and omit duplicate copies of already-defined Given/Then/When phrases so the existing definitions bind. Do not change those existing step implementations.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hardcoding `return True` instead of `greet(name).startswith("Hello, ")` | Med | High | Implement as `return greet(name).startswith("Hello, ")`; AC1/AC2 assert equality with startswith |
| Checking `name.startswith("Hello, ")` instead of `greet(name).startswith("Hello, ")` | Med | High | Body is exactly `return greet(name).startswith("Hello, ")` |
| Returning `"True"` / `"False"` strings | Med | High | Unit and BDD asserts use `is True` |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greeting_starts_with_hello` |
| CLI, `greet`, `greeting_length`, or `greeting_is_ascii` edits | Low | High | Leave `cli.py` and those function bodies/signatures untouched |
| Treating Ada as the only exercised name | Med | High | AC2 uses `Jo` and asserts `greet("Jo") != greet("Ada")` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #68 | 2026-09-01 | Initial feature spec |
