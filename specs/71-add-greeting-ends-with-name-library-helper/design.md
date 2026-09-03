# Design: Add greeting_ends_with_name library helper

**Issue**: #71
**Date**: 2026-09-03
**Status**: Approved
**Author**: NMG
---

## Overview

Add a pure library function `greeting_ends_with_name(name: str) -> bool` immediately after `greeting_starts_with_hello` in `src/nmg_sdlc_smoke/greet.py`. It returns `greet(name).endswith(name)` so the result is the Python bool for whether the current greeting string ends with the same supplied name. Invalid names propagate `greet`'s `ValueError("name must not be blank")` unwrapped. Export `greeting_ends_with_name` from `src/nmg_sdlc_smoke/__init__.py` without dropping `greet`, `greet_many`, `greeting_bytes`, `greeting_is_ascii`, `greeting_length`, `greeting_starts_with_hello`, or any already-exported names. Do not change `greet`, existing helpers, `cli.py`, the console script, or `VERSION`. Requirements: `specs/71-add-greeting-ends-with-name-library-helper/requirements.md`.

No equivalent suffix helper exists. Do not add a new module.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                           │
│  from nmg_sdlc_smoke import greet, greet_many,             │
│                            greeting_bytes,                 │
│                            greeting_is_ascii,              │
│                            greeting_length,                │
│                            greeting_starts_with_hello,     │
│                            greeting_ends_with_name         │
│  greeting_ends_with_name(name) → bool                      │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│  nmg_sdlc_smoke.greet                                      │
│  greet(name: str) -> str  (unchanged)                      │
│  existing helpers unchanged                                │
│  ValueError("name must not be blank")                      │
│  greeting_ends_with_name(name: str) -> bool                │
│    return greet(name).endswith(name)                       │
└──────────────────────────────────────────────────────────┘
```


CLI nmg_sdlc_smoke.cli:main is unchanged and does not call greeting_ends_with_name.


### Data Flow

```
1. Caller invokes greeting_ends_with_name(name)
2. greeting_ends_with_name calls greet(name)
3. If greet raises ValueError("name must not be blank"), that exception propagates unwrapped
4. Otherwise return greeting.endswith(name)
5. Examples: greeting_ends_with_name("Ada") is True because greet("Ada") == "Hello, Ada"
             greeting_ends_with_name("Jo") is True because greet("Jo") == "Hello, Jo"
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `greeting_ends_with_name(name: str) -> bool` | library function | No | whether `greet(name)` ends with the same `name` |

Append `greeting_ends_with_name` to `nmg_sdlc_smoke.__all__` after the existing public names. Current `src/nmg_sdlc_smoke/__init__.py` is:

```python
from .greet import greet, greet_many
from .greet import greeting_bytes as greeting_bytes
from .greet import greeting_is_ascii as greeting_is_ascii
from .greet import greeting_length as greeting_length
from .greet import greeting_starts_with_hello as greeting_starts_with_hello

__all__ = [
    "greet",
    "greet_many",
    "greeting_bytes",
    "greeting_is_ascii",
    "greeting_length",
    "greeting_starts_with_hello",
]
```

Change it by adding one import alias and one `__all__` entry, keeping every existing name:

```python
from .greet import greet, greet_many
from .greet import greeting_bytes as greeting_bytes
from .greet import greeting_ends_with_name as greeting_ends_with_name
from .greet import greeting_is_ascii as greeting_is_ascii
from .greet import greeting_length as greeting_length
from .greet import greeting_starts_with_hello as greeting_starts_with_hello

__all__ = [
    "greet",
    "greet_many",
    "greeting_bytes",
    "greeting_ends_with_name",
    "greeting_is_ascii",
    "greeting_length",
    "greeting_starts_with_hello",
]
```

If another public helper is already imported and listed in `__all__` when this issue is implemented, keep those names and still export `greeting_ends_with_name`. Alphabetical placement of the new alias among the `from .greet import ... as ...` lines is allowed; do not drop names.

`greet` stays `greet(name: str) -> str`. `main(argv: list[str] | None = None) -> int` stays. Do not edit `src/nmg_sdlc_smoke/cli.py`.

Implementation in `greet.py` immediately after `greeting_starts_with_hello`. No equivalent suffix helper exists:

```python
def greeting_ends_with_name(name: str) -> bool:
    return greet(name).endswith(name)
```

Do not reimplement blank-name checks in `greeting_ends_with_name`. Do not `return True`. Do not call `name.endswith(name)` without going through `greet`. Do not return `"True"` / `"False"` strings. Do not implement case-insensitive comparison, configurable suffix, or normalization.

### Request / Response Schemas

#### greeting_ends_with_name(name)

**Input:** a name (`str`). Same contract as `greet`.

**Output (success):** Python `bool` equal to `greet(name).endswith(name)`. Examples: `greeting_ends_with_name("Ada") is True`; `greeting_ends_with_name("Jo") is True`.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `ValueError("name must not be blank")` | blank, whitespace-only, or non-string `name`; raised by `greet`, not wrapped |

#### greet(name) and nmg-smoke NAME (unchanged)

**Input / output / errors:** unchanged. `greet("Ada")` remains `Hello, Ada`. `nmg-smoke Ada` still exits `0`, writes `Hello, Ada\n` to stdout, and writes nothing to stderr. Blank names still raise `ValueError` from `greet` and still cause the CLI to exit non-zero without a stdout greeting.

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
| **A: `return greet(name).endswith(name)` in `greet.py`** | Reuse greeting and validation | Always matches live `greet` suffix; one module; no extra validation | Callers import a second symbol | **Selected** |
| **B: `return True`** | Constant because current format ends with `{name}` | Slightly less work | Diverges if greeting format changes; violates AC1/AC2 equality | Rejected |
| **C: `return name.endswith(name)`** | Skip `greet` | Slightly less work | Out of scope; ignores greeting contract and validation | Rejected |
| **D: new module or CLI flag** | Separate file / shell visibility | Isolation / discoverable | Extra module or CLI change against structure steering / out of scope | Rejected |

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
| Library | Unit `tests/test_greet.py` | Ada → `True` and equals `greet("Ada").endswith("Ada")`; Jo → `True` and equals `greet("Jo").endswith("Jo")` and not Ada-only; blank/whitespace/non-string `ValueError`; existing `greet` / helper tests unchanged |
| CLI | Unit `tests/test_cli.py` | untouched; existing Ada / blank-name tests cover AC4 CLI |
| Feature | pytest-bdd `tests/features/add_greeting_ends_with_name_library_helper.feature` | AC1–AC4 as `@SCN001`–`@SCN004` |
| Lint | Ruff | `src` and `tests` |

Keep calling `greet` / `greeting_ends_with_name` in-process, matching `tests/test_greet.py`. Do not hardcode a VERSION literal. CLI assertions in AC4 call `nmg_sdlc_smoke.cli.main(["Ada"])` with `capsys`, matching `tests/test_cli.py` and `tests/features/steps/test_greeting_starts_with_hello_steps.py`.

Register the new feature with a new steps module `tests/features/steps/test_greeting_ends_with_name_steps.py` calling `scenarios("../add_greeting_ends_with_name_library_helper.feature")`. Do not add a second `scenarios(...)` to existing step modules. Do not edit `pyproject.toml` pytest markers; reuse existing `@SCN001`–`@SCN004` marker names.

Gherkin step texts (executable feature omits spec frontmatter):

- Unique Given/When/Then texts that must live only in `test_greeting_ends_with_name_steps.py`: `Given the installed package is importable`; `Given greeting_ends_with_name is imported from the public package`; `When greeting_ends_with_name is called with Ada`; `And that value equals greet Ada endswith Ada`; `When greeting_ends_with_name is called with Jo`; `And that value equals greet Jo endswith Jo`; `And the result is not specific to the Ada example`; `When greeting_ends_with_name is called with a blank, whitespace-only, or non-string name`.
- Reuse existing phrases for AC4 and shared Then text so pytest-bdd can bind them: `Then it returns True`; `Then it raises ValueError with message name must not be blank`; `And that error is the existing greet validation error, not a wrapped or renamed error`; `Given the distribution is installed`; `When greet is called with Ada`; `Then it returns Hello, Ada`; `When nmg-smoke Ada is run`; `Then the process exits 0 and prints Hello, Ada followed by a single newline`; `And blank names still raise ValueError from greet and still cause the CLI to exit non-zero without a stdout greeting`.
- Unique Given importable: `assert callable(greet)` and `assert callable(greeting_ends_with_name)`.
- Unique Given imported: `assert callable(greeting_ends_with_name)`.
- Unique When Ada/Jo: store `greeting_ends_with_name("Ada")` / `greeting_ends_with_name("Jo")` in `context["result"]`.
- Unique Then for Ada suffix: `assert greet("Ada") == "Hello, Ada"` and `assert context["result"] is True` and `assert context["result"] == greet("Ada").endswith("Ada")`.
- Unique Then for Jo suffix: `assert greet("Jo") == "Hello, Jo"` and `assert context["result"] is True` and `assert context["result"] == greet("Jo").endswith("Jo")`.
- Unique Then not specific to Ada: `assert context["result"] == greet("Jo").endswith("Jo")` and `assert greet("Jo") != greet("Ada")` and `assert greeting_ends_with_name("Ada") is True`.
- Unique invalid-name When must populate `context["errors"]` and `context["greet_errors"]` the same way as `tests/features/steps/test_greeting_starts_with_hello_steps.py` (values `""`, `" "`, `"\t"`, `"\n"`, `None`, `42`; compare type+message; `__cause__` and `__context__` are `None`).
- If a local `Then it returns True` is required because pytest-bdd does not bind the existing step, `assert context["result"] is True` (identity, not string compare).

If pytest-bdd rejects duplicate step definitions across modules, keep the unique Given/When/Then texts in `test_greeting_ends_with_name_steps.py` and omit duplicate copies of already-defined Given/Then/When phrases so the existing definitions bind. Do not change those existing step implementations.

Do not use Given phrase `the library is importable` in this feature; that existing step only asserts `greet` and `greeting_starts_with_hello` and would not prove the new helper is importable.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Hardcoding `return True` instead of `greet(name).endswith(name)` | Med | High | Implement as `return greet(name).endswith(name)`; AC1/AC2 assert equality with endswith |
| Checking `name.endswith(name)` instead of `greet(name).endswith(name)` | Med | High | Body is exactly `return greet(name).endswith(name)` |
| Returning `"True"` / `"False"` strings | Med | High | Unit and BDD asserts use `is True` |
| Wrapping `greet` `ValueError` | Med | High | Do not catch `ValueError` inside `greeting_ends_with_name` |
| CLI or `greet` edits | Low | High | Leave `cli.py` and the `greet` body/signature untouched |
| Treating Ada as the only exercised name | Med | High | AC2 uses `Jo` and asserts `greet("Jo") != greet("Ada")` |
| Dropping an existing public export | Med | High | Append `greeting_ends_with_name`; keep current `__all__` names |

---
## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #71 | 2026-09-03 | Initial feature spec |
