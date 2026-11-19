# Tasks: Add greeting_slug library helper

**Issue**: #326
**Date**: 2026-11-19
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_slug

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `import re` and `import unicodedata` in sorted position, and add `greeting_slug(name: str) -> str` exactly as in design.md immediately after `greeting_reversed` (AC1, AC2, AC3, AC4, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_slug as greeting_slug` immediately after the `greeting_shake_256` import;
  - add the `__all__` entry `"greeting_slug"` immediately after `"greeting_shake_256"`;
  - remove no existing export (AC5, FR3, FR5).
- In README `## Library`:
  - add `greeting_slug,` after `greeting_shake_256,` in the import list;
  - add the `greeting_slug("Ada Lovelace")  # "hello-ada-lovelace"` example after the `greeting_reversed("Ada")  # "adA ,olleH"` example;
  - add the exact `greeting_slug` prose line from design.md after the `greeting_reversed` prose line (AC5, FR4).
- `python -m ruff check .` passes.

### T002: Exercise five AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_slug_library_helper.feature`, `tests/features/steps/test_greeting_slug_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the five tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_slug_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_initials_steps.py` (AC1–AC5).
- Assert:
  - `"hello-ada"`, `"hello-ada-lovelace"`, `"hello-ada-lovelace"`, and `"hello-agent-007"` for `"Ada"`, `"Ada Lovelace"`, `"Ada \t Lovelace"`, and `"Agent 007"`, each of type `str` (AC1);
  - `"hello-o-brien"`, `"hello-ada"`, `"hello-ada"`, and `"hello-ada-lovelace"` for `"O'Brien"`, `"Ada!!"`, `"--Ada--"`, and `"Ada_Lovelace"`, and no result contains `--` or starts or ends with `-` (AC2);
  - `"hello-zoe"`, `"hello-emile"`, `"hello-ada"`, and `"hello-ada-lee"` for `"Zoë"`, `"ÉMILE"`, `"Ａda"`, and `"Ada李Lee"`, each fully matching `^[a-z0-9]+(-[a-z0-9]+)*$` (AC3);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC4);
  - the README example and unchanged CLI (AC5), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_slug("Ada Lovelace"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
    - the run gives `(returncode, stdout, stderr) == (0, "hello-ada-lovelace\n", "")`;
    - `"greeting_slug" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_reversed`, `greeting_shake_256`, `greeting_space_count`, and `greeting_initials`) remains;
    - the exact `greeting_slug` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_slug_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #326 | 2026-11-19 | Initial feature tasks |
