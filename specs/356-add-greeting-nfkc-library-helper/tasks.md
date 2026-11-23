# Tasks: Add greeting_nfkc library helper

**Issue**: #356
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_nfkc

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_nfkc(name: str) -> str` exactly as in design.md, immediately after `greeting_nfd` (AC1, AC2, AC3, AC4, AC5, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_nfkc as greeting_nfkc` immediately after the `greeting_nfd` import;
  - add the `__all__` entry `"greeting_nfkc"` immediately after `"greeting_nfd"`;
  - remove no existing export (AC6, FR3).
- In README `## Library`:
  - add `greeting_nfkc,` after `greeting_nfd,` in the import list;
  - add the `greeting_nfkc("ﬁona")  # "Hello, fiona"` example after the `len(greeting_nfd("Chloé"))  # 13` example;
  - add the exact `greeting_nfkc` prose line from design.md after the `greeting_nfd` prose line (AC6, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_nfkc_library_helper.feature`, `tests/features/steps/test_greeting_nfkc_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the six tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_nfkc_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_nfd_steps.py`. Write non-ASCII inputs and expectations as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Hello, fiona"` (length 12) for `"\N{LATIN SMALL LIGATURE FI}ona"`, `"Hello, Ada"` (length 10) for `"\N{FULLWIDTH LATIN CAPITAL LETTER A}\N{FULLWIDTH LATIN SMALL LETTER D}\N{FULLWIDTH LATIN SMALL LETTER A}"`, and `"Hello, Ada Lovelace"` (length 19) for `"Ada\N{NO-BREAK SPACE}Lovelace"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): assert `"Hello, Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` (length 12) for `"Chloe\N{COMBINING ACUTE ACCENT}"`.
- `@SCN003` (AC3): for `"Ada"`, `"Ada  Lovelace"`, and `"O'Brien-Smith"`, assert `result == greet(name)`.
- `@SCN004` (AC4): for `"Ada"`, `"Chloe\N{COMBINING ACUTE ACCENT}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `"O'Brien-Smith"`, assert `result == unicodedata.normalize("NFKC", greet(name))` and `unicodedata.is_normalized("NFKC", result)`.
- `@SCN005` (AC5): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN006` (AC6):
  - `from nmg_sdlc_smoke import greeting_nfkc` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_nfkc("ﬁona"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Hello, fiona\n", "")`;
  - `"greeting_nfkc" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_nfc`, `greeting_nfd`, `greeting_md5`, `greeting_punctuation_count`, and `greeting_swapcase`;
  - the exact `greeting_nfkc` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_nfkc_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #356 | 2026-11-23 | Initial feature tasks |
