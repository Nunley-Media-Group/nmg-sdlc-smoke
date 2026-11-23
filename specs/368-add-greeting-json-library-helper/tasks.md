# Tasks: Add greeting_json library helper

**Issue**: #368
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_json

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `import json` after `import html` and add `greeting_json(name: str) -> str` exactly as in design.md, immediately after `greeting_html_escaped` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_json as greeting_json` immediately after the `greeting_is_title` import;
  - add the `__all__` entry `"greeting_json"` immediately after `"greeting_is_title"`;
  - remove no existing export (AC4, FR3).
- In README `## Library`:
  - add `greeting_json,` after `greeting_is_title,` in the import list;
  - add the `greeting_json("Ada")  # '"Hello, Ada"'` example after the `greeting_html_escaped("<Ada & Bo>")` example;
  - add the exact `greeting_json` prose line from design.md after the `greeting_html_escaped` prose line (AC4, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_json_library_helper.feature`, `tests/features/steps/test_greeting_json_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_json_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_html_escaped_steps.py`. Write non-ASCII inputs as Python `\N{...}` escapes and expected escaped outputs as raw strings.
- `@SCN001` (AC1): assert `'"Hello, Ada"'` for `"Ada"` and `'"Hello, Ada Lovelace"'` for `"Ada Lovelace"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `r'"Hello, Ada \"Bo\""'` for `'Ada "Bo"'`, `r'"Hello, C:\\x"'` for `"C:\\x"`, `r'"Hello, Ada\tBo"'` for `"Ada\tBo"`, and `r'"Hello, \u00c9mile"'` for `"\N{LATIN CAPITAL LETTER E WITH ACUTE}mile"`; for each, assert the result equals `json.dumps(greet(name))`, `result.isascii()` is `True`, and `json.loads(result) == greet(name)`.
- `@SCN003` (AC3): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN004` (AC4):
  - `from nmg_sdlc_smoke import greeting_json` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_json("Ada"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, '"Hello, Ada"\n', "")`;
  - `"greeting_json" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_html_escaped`, `greeting_is_title`, `greeting_last_word`, `greeting_capitalize`, and `greeting_word_frequency`;
  - the exact `greeting_json` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_json_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #368 | 2026-11-23 | Initial feature tasks |
