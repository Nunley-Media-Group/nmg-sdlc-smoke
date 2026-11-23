# Tasks: Add greeting_nfd library helper

**Issue**: #350
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_nfd

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_nfd(name: str) -> str` exactly as in design.md, immediately after `greeting_nfc` (AC1, AC2, AC3, AC4, AC5, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_nfd as greeting_nfd` immediately after the `greeting_nfc` import;
  - add the `__all__` entry `"greeting_nfd"` immediately after `"greeting_nfc"`;
  - remove no existing export (AC6, FR3).
- In README `## Library`:
  - add `greeting_nfd,` after `greeting_nfc,` in the import list;
  - add the `len(greeting_nfd("Chlo\u00e9"))  # 13` example after the `greeting_nfc("Chloe\u0301")` example;
  - add the exact `greeting_nfd` prose line from design.md after the `greeting_nfc` prose line (AC6, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_nfd_library_helper.feature`, `tests/features/steps/test_greeting_nfd_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the six tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_nfd_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_nfc_steps.py`. Write non-ASCII inputs and expectations as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert `"Hello, Chloe\N{COMBINING ACUTE ACCENT}"` (length 13) for `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"` and `"Hello, A\N{COMBINING RING ABOVE}ngstro\N{COMBINING DIAERESIS}m"` (length 17) for `"\N{LATIN CAPITAL LETTER A WITH RING ABOVE}ngstr\N{LATIN SMALL LETTER O WITH DIAERESIS}m"`; assert `type(result) is str` for each.
- `@SCN002` (AC2): for `"Ada"`, `"Ada Lovelace"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`, assert `result == greet(name)`.
- `@SCN003` (AC3): assert `"Hello, \N{LATIN SMALL LIGATURE FI}ona"` (length 11) for `"\N{LATIN SMALL LIGATURE FI}ona"` and `"Hello, Ada  Lovelace"` for `"Ada  Lovelace"`.
- `@SCN004` (AC4): for `"Ada"`, `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `"O'Brien-Smith"`, assert `result == unicodedata.normalize("NFD", greet(name))` and `unicodedata.is_normalized("NFD", result)`.
- `@SCN005` (AC5): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN006` (AC6):
  - `from nmg_sdlc_smoke import greeting_nfd` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(len(greeting_nfd("Chlo\u00e9")))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "13\n", "")`;
  - `"greeting_nfd" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_nfc`, `greeting_md5`, `greeting_punctuation_count`, and `greeting_swapcase`;
  - the exact `greeting_nfd` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_nfd_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #350 | 2026-11-23 | Initial feature tasks |
