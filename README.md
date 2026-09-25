# nmg-sdlc-smoke-python

A disposable Python SDLC smoke host used to exercise issue-to-spec-to-delivery workflows against a small, independently verifiable project.

## Requirements

- Python 3.12 or newer
- `VERSION` is the release source of truth; `pyproject.toml` reads it dynamically

## Install

```console
python -m pip install -e ".[dev]"
```

## Library

```python
from nmg_sdlc_smoke import (
    greet,
    greet_many,
    greeting_bytes,
    greeting_casefold,
    greeting_ends_with_exclamation,
    greeting_ends_with_name,
    greeting_has_asterisk,
    greeting_has_at_sign,
    greeting_has_backtick,
    greeting_has_colon,
    greeting_has_equal,
    greeting_has_hash,
    greeting_has_percent,
    greeting_has_plus,
    greeting_has_question_mark,
    greeting_has_semicolon,
    greeting_is_ascii,
    greeting_length,
    greeting_starts_with_hello,
    greeting_word_count,
)

greet("Ada")  # "Hello, Ada"
greeting_ends_with_exclamation("Ada")  # "Hello, Ada!"
greet_many(["Ada", "Bob"])  # ["Hello, Ada", "Hello, Bob"]
greeting_length("Ada")  # 10
greeting_bytes("Ada")  # 10
greeting_is_ascii("Ada")  # True
greeting_casefold("Straße")  # "hello, strasse"
greeting_starts_with_hello("Ada")  # True
greeting_ends_with_name("Ada")  # True
greeting_has_asterisk("Ada*")  # True
greeting_has_asterisk("Ada")  # False
greeting_has_asterisk("Ada∗")  # False
greeting_has_backtick("Ada`")  # True
greeting_has_backtick("Ada")  # False
greeting_has_backtick("Ada｀")  # False
greeting_has_at_sign("Ada@")  # True
greeting_has_at_sign("Ada")  # False
greeting_has_colon("Ada:")  # True
greeting_has_colon("Ada")  # False
greeting_has_equal("Ada=")  # True
greeting_has_equal("Ada")  # False
greeting_has_equal("Ada＝")  # False
greeting_has_hash("Ada#")  # True
greeting_has_hash("Ada")  # False
greeting_has_percent("Ada%")  # True
greeting_has_percent("Ada")  # False
greeting_has_plus("Ada+")  # True
greeting_has_plus("Ada")  # False
greeting_has_question_mark("Ada?")  # True
greeting_has_question_mark("Ada")  # False
greeting_has_semicolon("Ada;")  # True
greeting_has_semicolon("Ada")  # False
greeting_word_count("Ada")  # 2
greeting_word_count("Ada Lovelace")  # 3
```

`greet` rejects blank, whitespace-only, and non-string names with `ValueError("name must not be blank")`.
`greeting_casefold` applies Unicode casefolding to the complete greeting and uses the same validation as `greet`; it does not change `greet` or CLI output.
`greeting_word_count` counts whitespace-separated words in the complete greeting using Python's `str.split()` semantics and the same validation as `greet`.
`greeting_has_semicolon` checks for a literal `;` in the complete greeting and uses the same name validation as `greet`.
`greeting_has_colon` checks for a literal `:` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_asterisk` matches only a literal ASCII `*` (U+002A) in the completed greeting, not U+2217 `∗`, and inherits `greet`'s `ValueError("name must not be blank")`.
`greeting_has_backtick` matches only a literal ASCII backtick (U+0060) in the complete greeting, not the fullwidth lookalike U+FF40, and inherits `greet`'s `ValueError("name must not be blank")`.
`greeting_has_at_sign` checks for a literal `@` in the completed greeting and uses the same name validation as `greet`.
`greeting_has_equal` matches only a literal ASCII `=` in the complete greeting (not a fullwidth `＝`) and inherits `greet`'s invalid-name `ValueError`.
`greeting_has_hash` checks for a literal `#` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_question_mark` checks for a literal `?` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_percent` checks for a literal `%` in the complete greeting and uses the same invalid-name validation as `greet`.
`greeting_has_plus` checks for a literal `+` in the complete greeting and uses the same invalid-name validation as `greet`.

## CLI

```console
$ nmg-smoke Ada
Hello, Ada
```

Use `--uppercase` to capitalize the complete greeting:

```console
$ nmg-smoke --uppercase Ada
HELLO, ADA
```

Use `--repeat COUNT` to print the greeting once per line:

```console
$ nmg-smoke --repeat 3 Ada
Hello, Ada
Hello, Ada
Hello, Ada
```

Use `--prefix TEXT` to prepend text exactly as supplied:

```console
$ nmg-smoke --prefix 'OK: ' Ada
OK: Hello, Ada
```

Use `--no-newline` to omit the trailing newline from successful output:

```console
$ nmg-smoke --no-newline Ada
Hello, Ada
```

The output above is exactly `Hello, Ada` without a trailing newline.

Use `--parentheses` to enclose each fully composed greeting in literal parentheses:

```console
$ nmg-smoke --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada
(ok: HELLO, ADA)
(ok: HELLO, ADA)
```

Uppercase applies before the literal prefix; parentheses wrap the complete message
once before repetition and newline handling. The example has one separating LF
and no final LF. Existing parentheses and internal newlines are preserved without
escaping. Without `--parentheses`, composed and default output remain unchanged.

Use `--braces` to enclose each fully formatted greeting in literal curly braces:

```console
$ nmg-smoke --braces --parentheses --uppercase --prefix 'ok: ' --repeat 2 --no-newline Ada
{(ok: HELLO, ADA)}
{(ok: HELLO, ADA)}
```

Braces wrap the complete message after parentheses and before repetition and
newline handling, so they are always outermost. Without `--braces`, composed
and default output remain byte-identical.

Use `--quotes` to enclose the fully composed greeting in literal double quotes:

```console
$ nmg-smoke --quotes --uppercase --prefix 'ok: ' --parentheses --braces Ada
"{(ok: HELLO, ADA)}"
```

Quotes wrap the complete message after braces and before repetition and newline
handling. Without `--quotes`, output remains byte-identical.

A blank name exits 1 and writes no greeting to stdout.

## Verification

```console
python -m pytest
python -m pytest tests/features
python -m ruff check .
```

Unit tests cover the library and CLI. pytest-bdd scenarios under `tests/features/` cover the approved acceptance criteria. Ruff checks `src/` and `tests/`. GitHub Actions runs the same Python checks on pull requests and pushes to `main`.

## Layout

- `src/nmg_sdlc_smoke/` — import package and console entry point
- `tests/` — pytest unit tests
- `tests/features/` — pytest-bdd features and steps
- `specs/` — current approved issue contracts
- `steering/` — product, technology, and structure guidance
- `VERSION` — 3.x version source synchronized into package metadata

This repository is intentionally minimal. Git history, not the working tree, archives the copied plugin that preceded the Python host.
