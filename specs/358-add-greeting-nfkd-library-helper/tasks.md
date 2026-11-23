# Tasks: Add greeting_nfkd library helper

**Issue**: #358
**Date**: 2026-11-23
**Status**: Approved
**Author**: NMG

## Implementation Tasks

### T001: Implement, export, and document greeting_nfkd

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `greeting_nfkd(name: str) -> str` exactly as in design.md, immediately after `greeting_nfkc` if present and otherwise after `greeting_nfd` (AC1, AC2, AC3, AC4, AC5, FR1, FR2).
- In `__init__.py`, using the same anchor:
  - add the self-aliased import `from .greet import greeting_nfkd as greeting_nfkd`;
  - add the `__all__` entry `"greeting_nfkd"`;
  - remove no existing export (AC6, FR3).
- In README `## Library`, using the same anchor:
  - add `greeting_nfkd,` to the import list;
  - add the `greeting_nfkd("\ufb01ona")  # "Hello, fiona"` example;
  - add the exact `greeting_nfkd` prose line from design.md (AC6, FR4).
- `python -m ruff check .` passes.

### T002: Implement the `feature.gherkin` scenarios

**File(s)**: `tests/features/add_greeting_nfkd_library_helper.feature`, `tests/features/steps/test_greeting_nfkd_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the six tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_nfkd_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_nfd_steps.py`. Write non-ASCII inputs and expectations as Python `\N{...}` escapes.
- `@SCN001` (AC1): assert these results, and assert `type(result) is str` for each:
  - `"Hello, fiona"` (length 12) for `"\N{LATIN SMALL LIGATURE FI}ona"`;
  - `"Hello, Ada"` (length 10) for `"\N{FULLWIDTH LATIN CAPITAL LETTER A}da"`;
  - `"Hello, Ada2"` (length 11) for `"Ada\N{SUPERSCRIPT TWO}"`.
- `@SCN002` (AC2): assert `"Hello, Chloe\N{COMBINING ACUTE ACCENT}"` (length 13) for `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`.
- `@SCN003` (AC3): for `"Ada"`, `"Ada  Lovelace"`, and `"Chloe\N{COMBINING ACUTE ACCENT}"`, assert `result == greet(name)`.
- `@SCN004` (AC4): for `"Ada"`, `"Chlo\N{LATIN SMALL LETTER E WITH ACUTE}"`, `"\N{LATIN SMALL LIGATURE FI}ona"`, and `"O'Brien-Smith"`, assert `result == unicodedata.normalize("NFKD", greet(name))` and `unicodedata.is_normalized("NFKD", result)`.
- `@SCN005` (AC5): assert `ValueError` with the exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42`.
- `@SCN006` (AC6):
  - `from nmg_sdlc_smoke import greeting_nfkd` succeeds;
  - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
  - append `print(greeting_nfkd("\ufb01ona"))` and run the result with `sys.executable -c` and `encoding="utf-8"`, with `PYTHONIOENCODING=utf-8` in the child environment;
  - the run gives `(returncode, stdout, stderr) == (0, "Hello, fiona\n", "")`;
  - `"greeting_nfkd" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` remains, including `greeting_nfc`, `greeting_nfd`, `greeting_md5`, `greeting_punctuation_count`, and `greeting_swapcase`;
  - the exact `greeting_nfkd` prose line from design.md is one of the lines of `README.md`.
- Run `python -m pytest tests/features/steps/test_greeting_nfkd_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #358 | 2026-11-23 | Initial feature tasks |
