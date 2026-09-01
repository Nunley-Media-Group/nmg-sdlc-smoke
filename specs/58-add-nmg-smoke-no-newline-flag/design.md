# Design: Add nmg-smoke --no-newline flag

**Issue**: #58
**Date**: 2026-09-01
**Status**: Approved
**Author**: NMG
---

## Overview

Extend the existing `nmg-smoke` argparse CLI with a long boolean `--no-newline` option. Successful output keeps the existing transformed message and all separators between repeated greetings, but omits the newline after the final greeting. Omitting the flag preserves the current newline-terminated output. The required positional name, `greet` validation, `greeting_length`, package exports, error paths, and existing `--uppercase`, `--repeat COUNT`, and `--prefix TEXT` semantics remain unchanged. Requirements: `specs/58-add-nmg-smoke-no-newline-flag/requirements.md`.

Live code in `src/nmg_sdlc_smoke/cli.py` parses the existing options and required name, calls `greet`, applies uppercase and prefix transformations, then runs `for _ in range(args.repeat): print(message)`. Add `parser.add_argument("--no-newline", action="store_true")`. Replace only the print loop with an indexed loop that selects `end=""` for the final iteration when the flag is set and `end="\n"` otherwise. This preserves inter-greeting separators without building or copying a repeated output string. Do not import `sys`, add a short option, or change library files.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main     │
│  argparse: required name + --uppercase + --repeat COUNT │
│            + --prefix TEXT + --no-newline               │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    Output Adapter                        │
│  Existing transformed message printed COUNT times       │
│  Newlines separate repetitions                          │
│  Final print end is "" only when --no-newline is set    │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                         │
│  greet(name: str) -> str and greeting_length unchanged  │
└──────────────────────────────────────────────────────────┘
```

No database, HTTP API, UI, persistent state, new module, or library API change.

### Data Flow

```
1. Caller invokes nmg-smoke [options] NAME.
2. argparse parses --no-newline as store_true; name stays required.
3. Existing parsing failures exit non-zero before greet and print no greeting.
4. greet(args.name) runs exactly once.
5. Existing ValueError path uses parser.exit(1, ...); stdout stays empty.
6. Existing transformations run in order:
   a. uppercase the greeting when --uppercase is set
   b. prepend args.prefix
7. For index in range(args.repeat):
   a. final = index == args.repeat - 1
   b. end = "" only when args.no_newline and final; otherwise "\n"
   c. print(message, end=end)
8. Return 0. Successful stderr stays empty.
```

Examples:

- `nmg-smoke Ada` → `Hello, Ada
`
- `nmg-smoke --no-newline Ada` → `Hello, Ada`
- `nmg-smoke --no-newline --repeat 3 Ada` → `Hello, Ada
Hello, Ada
Hello, Ada`
- `nmg-smoke --no-newline --uppercase Ada` → `HELLO, ADA`
- `nmg-smoke --no-newline --prefix 'OK: ' Ada` → `OK: Hello, Ada`

The prefix example records composition only; it does not change the #52 prefix contract.

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg-smoke --no-newline NAME` | console option | No | Omit only the final successful stdout newline |

No new public Python function. `main(argv: list[str] | None = None) -> int` stays unchanged. `greet.py` and `__init__.py` are untouched.

Add this parser declaration before the required positional `name`:

```python
parser.add_argument("--no-newline", action="store_true")
```

After the existing uppercase and prefix transforms, replace the print loop with:

```python
for index in range(args.repeat):
    end = "" if args.no_newline and index == args.repeat - 1 else "\n"
    print(message, end=end)
```

Do not use `"\n".join([message] * args.repeat)`: the indexed loop avoids a repeated list and combined output allocation. Do not use `print(message, end="")` for every iteration because that would remove required separators.

### Request / Response Schemas

#### nmg-smoke --no-newline NAME

**Input:** argv contains the boolean `--no-newline` token and required positional `name`. The flag may appear before or after the name. It takes no value.

**Output (success):** `main` returns 0; stdout is the existing transformed greeting sequence with no newline after the last greeting; stderr is empty.

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| argparse non-zero | missing required name; no greeting on stdout |
| argparse non-zero | existing invalid or missing `--repeat COUNT`; no greeting on stdout |
| exit `1` | blank or whitespace-only name reaches existing `greet` `ValueError`; no greeting on stdout |

#### nmg-smoke NAME (unchanged)

**Output (success):** `Hello, Ada
` for `Ada`; `main` returns 0; stderr is empty.

#### greet(name) and greeting_length(name) (unchanged)

`greet("Ada") == "Hello, Ada"`; `greeting_length("Ada") == 10`. Blank, whitespace-only, and non-string names retain the existing `ValueError("name must not be blank")` library contract.

---

## Database / Storage Changes

None. No database.

---

## State Management

None. The per-iteration `end` value is invocation-local output state.

---

## UI Components

None. CLI only.

---

## Alternatives Considered

| Option | Description | Pros | Cons | Decision |
|--------|-------------|------|------|----------|
| **A: indexed print loop with final-iteration `end`** | Keep `print`; choose empty end only for the flagged final iteration | Preserves separators; no combined-output allocation; minimal change | One index comparison per iteration | **Selected** |
| **B: `print(message, end="" if flag else "\n")` on every iteration** | Change only the `end` argument | Smallest textual edit | Concatenates repeated greetings with no separators | Rejected |
| **C: join repeated messages into one string** | Build `"\n".join(...)` then print once | Simple final terminator | Allocates a repeated list and combined string | Rejected |
| **D: `sys.stdout.write`** | Write exact output directly | Explicit bytes-on-stream shape | New import and needless second output convention | Rejected |
| **E: short `-n` alias** | Add a conventional short flag | Faster typing | FR5 forbids it | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Existing argparse and `greet` validation remain authoritative
- [x] **Data Sanitization**: Greeting and prefix text handling remain unchanged
- [x] **Sensitive Data**: None

---

## Performance Considerations

- [x] **Allocations**: No repeated list or combined output string; each greeting is printed once
- [x] **Caching**: None
- [x] **Pagination**: None
- [x] **Lazy Loading**: None
- [x] **Indexing**: None

---

## Testing Strategy

| Layer | Type | Coverage |
|-------|------|----------|
| CLI | Unit `tests/test_cli.py` | flag before/after name; default newline; repeat 1 and 3; uppercase; missing name; blank names; empty stderr |
| Library | Unit `tests/test_greet.py` | Untouched; existing `greet` and `greeting_length` tests remain AC7 proof |
| Feature | pytest-bdd `tests/features/add_nmg_smoke_no_newline_flag.feature` | AC1–AC7 as `@SCN001`–`@SCN007` |
| Lint | Ruff | `src` and `tests` |

Call `main([...])` in-process with `capsys`, matching `tests/test_cli.py`. Happy paths return 0. Missing name raises `SystemExit` with non-zero code and empty stdout. Blank names with the flag raise `SystemExit` code 1, leave stdout empty, and report `name must not be blank` on stderr.

Register the new feature with `tests/features/steps/test_no_newline_steps.py` calling `scenarios("../add_nmg_smoke_no_newline_flag.feature")`. Set `pytest_plugins = ["test_greeting_steps", "test_uppercase_steps", "test_repeat_steps"]` to reuse existing distribution, default-output, blank-name, missing-name, and empty-stderr steps. Do not add another `scenarios(...)` call to existing step modules and do not redefine imported step texts.

Unique no-newline steps must assert exact strings, including absence of the final `
`:

- `nmg-smoke --no-newline Ada is run` invokes `main(["--no-newline", "Ada"])`.
- `stdout is exactly Hello, Ada with no trailing newline` asserts `captured.out == "Hello, Ada"`.
- The position-equivalence step invokes `main(["Ada", "--no-newline"])` after clearing captured output.
- The repeated step invokes `main(["--no-newline", "--repeat", "3", "Ada"])` and asserts `Hello, Ada
Hello, Ada
Hello, Ada`.
- The uppercase step invokes `main(["--no-newline", "--uppercase", "Ada"])` and asserts `HELLO, ADA`.
- The missing-name and blank-name steps exercise the existing `SystemExit` paths.
- The library scenario imports and calls `greet` and `greeting_length` directly and parametrizes `""`, `" "`, `"\t"`, `"\n"`, `None`, and `42` for the unchanged `ValueError` contract.

Do not edit pytest marker configuration; reuse existing `@SCN001` through `@SCN007` markers.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Every newline is removed under repeat | Med | High | Empty `end` only on the final indexed iteration; AC3 exact stdout |
| Default output loses its newline | Med | High | Default `store_true` value is false; AC2 preserves `Hello, Ada
` |
| Flag makes name optional | Low | High | Keep `parser.add_argument("name")` unchanged; AC5 |
| Failure path prints partial stdout | Low | High | Validate with `greet` before entering the output loop; AC6 |
| Library API gains newline state | Low | High | Touch only `cli.py`; AC7 |
| Repeated output is built in memory | Low | Med | Preserve streaming print loop; no join/list multiplication |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #58 | 2026-09-01 | Initial feature spec |
