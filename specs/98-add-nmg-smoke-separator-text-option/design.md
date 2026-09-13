# Design: Add nmg-smoke --separator TEXT option

**Issue**: #98
**Date**: 2026-09-07
**Status**: Approved
**Author**: NMG
---

## Overview

Extend the existing `nmg-smoke` argparse CLI with a long `--separator TEXT` option. TEXT is inserted only between repeated rendered greetings. Omitting the option keeps the current newline between repeats. The final terminator newline stays under `--no-newline`. `greet`, package exports, `--uppercase`, `--prefix TEXT`, `--repeat COUNT` validity, the required positional name, and error paths stay unchanged. Requirements: `specs/98-add-nmg-smoke-separator-text-option/requirements.md`.

Live code in `src/nmg_sdlc_smoke/cli.py` parses `--uppercase`, `--repeat COUNT`, `--prefix TEXT`, `--no-newline`, and required `name`; calls `greet` once; applies uppercase then prefix; then prints in an indexed loop that sets `end = ""` only for the final iteration when `--no-newline` is set, otherwise `"\n"`. Add `parser.add_argument("--separator", default="\n", metavar="TEXT")` with no short option. In the loop, non-final iterations use `end = args.separator`; the final iteration still uses `""` if `--no-newline` else `"\n"`. Do not join a combined output string. Do not import `sys`. Do not change library files.

---

## Architecture

### Component Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                    │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main     │
│  argparse: required name + --uppercase + --repeat COUNT │
│            + --prefix TEXT + --no-newline               │
│            + --separator TEXT (default "\\n")           │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    Output Adapter                        │
│  Existing transformed message printed COUNT times       │
│  Non-final print end is args.separator                  │
│  Final print end is "" only when --no-newline is set    │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    Library Layer                         │
│  greet(name: str) -> str unchanged                      │
└──────────────────────────────────────────────────────────┘
```

No database, HTTP API, UI, persistent state, new module, or library API change.

### Data Flow

```
1. Caller invokes nmg-smoke [options] NAME.
2. argparse parses --separator TEXT; default is "\n"; name stays required.
3. Existing parsing failures exit non-zero before greet and print no greeting.
4. greet(args.name) runs exactly once.
5. Existing ValueError path uses parser.exit(1, ...); stdout stays empty.
6. Existing transformations run in order:
   a. uppercase the greeting when --uppercase is set
   b. prepend args.prefix
7. For index in range(args.repeat):
   a. if index is last: end = "" if args.no_newline else "\n"
   b. else: end = args.separator
   c. print(message, end=end)
8. Return 0. Successful stderr stays empty.
```

Authorized examples:

- `nmg-smoke --repeat 2 --separator ' | ' Ada` → `Hello, Ada | Hello, Ada\n`
- `nmg-smoke --repeat 2 Ada` → `Hello, Ada\nHello, Ada\n`

`--no-newline` composition is not an acceptance criterion. The loop above keeps its current final-terminator rule so #58 stays intact without extra Gherkin.

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg-smoke --separator TEXT NAME` | console option | No | Insert TEXT between repeated greetings |

No new public Python function. `main(argv: list[str] | None = None) -> int` stays unchanged. `greet.py` and `__init__.py` are untouched.

Add this parser declaration after `--no-newline` and before required positional `name`:

```python
parser.add_argument("--separator", default="\n", metavar="TEXT")
```

Replace the print loop with:

```python
for index in range(args.repeat):
    if index == args.repeat - 1:
        end = "" if args.no_newline else "\n"
    else:
        end = args.separator
    print(message, end=end)
```

Do not use `"\n".join([message] * args.repeat)`. Do not add `-s`.

### Request / Response Schemas

#### nmg-smoke --repeat 2 --separator TEXT NAME

**Input:** argv `["--repeat", "2", "--separator", " | ", "Ada"]` for AC1. TEXT is space-pipe-space.

**Output (success):** `main` returns 0; stdout is exactly `Hello, Ada | Hello, Ada\n`; stderr is empty.

**Errors:** unchanged existing argparse and `greet` `ValueError` paths. Missing-TEXT and empty TEXT are not acceptance criteria and must not gain Gherkin scenarios. Bare `--separator` without a TEXT token follows existing argparse required-value behavior for `--prefix`.

#### nmg-smoke --repeat 2 NAME (unchanged)

**Output (success):** stdout `Hello, Ada\nHello, Ada\n` for `Ada`; `main` returns 0; stderr is empty.

#### greet(name) (unchanged)

`greet("Ada") == "Hello, Ada"`. Blank, whitespace-only, and non-string names retain `ValueError("name must not be blank")`.

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
| **A: default `"\n"` plus non-final `end = args.separator`** | Keep streaming `print`; only the join text changes | Preserves #45/#58; no combined-output allocation | One branch per iteration | **Selected** |
| **B: join then one print** | Build a combined string then print once | Simple terminator | Allocates a repeated list and combined string | Rejected |
| **C: short `-s` alias** | Add a short flag | Faster typing | FR4 forbids it | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: Existing argparse and `greet` validation remain authoritative
- [x] **Data Sanitization**: Separator TEXT is printed as supplied between greetings
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
| CLI | Unit `tests/test_cli.py` | AC1 exact stdout; AC2 exact stdout; empty stderr; exit 0 |
| Library | Unit `tests/test_greet.py` | Untouched |
| Feature | pytest-bdd `tests/features/add_nmg_smoke_separator_text_option.feature` | AC1–AC2 as `@SCN001`–`@SCN002` only |
| Lint | Ruff | `src` and `tests` |

Call `main([...])` in-process with `capsys`, matching `tests/test_cli.py`.

Register the new feature with `tests/features/steps/test_separator_steps.py` calling `scenarios("../add_nmg_smoke_separator_text_option.feature")`. Set `pytest_plugins = ["test_greeting_steps", "test_repeat_steps", "test_no_newline_steps"]` to reuse the shared distribution Given, `Then the process exits 0`, and `And stderr is empty`. Do not add another `scenarios(...)` call to existing step modules and do not redefine imported step texts.

Unique steps:

- `nmg-smoke --repeat 2 --separator ' | ' Ada is run` invokes `main(["--repeat", "2", "--separator", " | ", "Ada"])`.
- `stdout is exactly Hello, Ada | Hello, Ada followed by a single newline` asserts `captured.out == "Hello, Ada | Hello, Ada\n"`.
- `nmg-smoke --repeat 2 Ada is run` invokes `main(["--repeat", "2", "Ada"])`.
- `stdout is exactly two lines of Hello, Ada, each followed by a newline` asserts `captured.out == "Hello, Ada\nHello, Ada\n"`.

Do not edit pytest marker configuration. Do not add `@SCN003` or later.

Feature-implementation tests and README edits must not bump `VERSION`. Delivery/open-pr owns the enhancement minor bump `3.32.0` → `3.33.0` and the `#98` CHANGELOG entry.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Default repeat output loses newlines | Med | High | Default `args.separator` is `"\n"`; AC2 exact stdout |
| Final terminator is replaced by TEXT | Med | High | Final iteration still uses `"\n"` unless `--no-newline`; AC1 keeps one trailing newline |
| Extra Gherkin is added during execute | Med | High | FR3 and feature.gherkin list only two scenarios |
| Delivery skips VERSION because issue said “do not bump VERSION” | Med | High | FR8 splits implementation vs delivery-owned minor bump |
| Library API gains separator state | Low | High | Touch only `cli.py` |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #98 | 2026-09-07 | Initial feature spec |
