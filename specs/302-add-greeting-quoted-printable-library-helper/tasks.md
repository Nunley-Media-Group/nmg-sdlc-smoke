# Tasks: Add greeting_quoted_printable library helper

**Issue**: #302
**Date**: 2026-11-13
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/293-add-greeting-html-escaped-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_quoted_printable

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `import quopri` after `import html`, and add `greeting_quoted_printable(name: str) -> str` returning `quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")` immediately after `greeting_html_escaped` (AC1, AC2, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_quoted_printable as greeting_quoted_printable` immediately after the `greeting_punctuation_count` import;
  - add the `__all__` entry `"greeting_quoted_printable"` immediately after `"greeting_punctuation_count"`;
  - remove no existing export (AC3, FR3, FR5).
- In README `## Library`:
  - add `greeting_quoted_printable,` after `greeting_punctuation_count,` in the import list;
  - add the `greeting_quoted_printable("Zoë")  # "Hello, Zo=C3=AB"` example after the `greeting_html_escaped("<Ada & Bo>")` example;
  - add the exact `greeting_quoted_printable` prose line from design.md after the `greeting_html_escaped` prose line (AC3, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `greeting_quoted_printable` to the package-root import list after `greeting_punctuation_count`; add `import quopri` to the test module imports if absent.
- Parameterize `("Ada", "Hello, Ada")`, `("Zoë", "Hello, Zo=C3=AB")`, `("a=b", "Hello, a=3Db")`, and `("Ada ", "Hello, Ada=20")`. For each, assert `type(result) is str`, the exact value, and equality with `quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")` (AC1).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC2).
- Assert `"greeting_quoted_printable" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_quoted_printable("Zoë") == "Hello, Zo=C3=AB"` (AC3).
- Run `python -m pytest tests/test_greet.py -k greeting_quoted_printable`.

### T003: Exercise three AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_quoted_printable_library_helper.feature`, `tests/features/steps/test_greeting_quoted_printable_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the three tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_quoted_printable_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_html_escaped_steps.py` (AC1–AC3).
- Assert:
  - the AC1 results `Hello, Ada`, `Hello, Zo=C3=AB`, `Hello, a=3Db`, and `Hello, Ada=20` for `"Ada"`, `"Zoë"`, `"a=b"`, and `"Ada "`, in that order, each a `str` equal to `quopri.encodestring(greet(name).encode("utf-8")).decode("ascii")` (AC1);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC2);
  - the README example and unchanged CLI (AC3), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_quoted_printable("Zoë"))` and run the result with `sys.executable -c` and `encoding="utf-8"` with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "Hello, Zo=C3=AB\n", "")`;
    - `"greeting_quoted_printable" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_punctuation_count` and `greeting_reversed`) remains;
    - the exact `greeting_quoted_printable` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_quoted_printable_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #302 | 2026-11-13 | Initial feature tasks |
