# Tasks: Add greeting_html_escaped library helper

**Issue**: #293
**Date**: 2026-11-08
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/217-add-greeting-url-encoded-library-helper/

## Implementation Tasks

### T001: Implement, export, and document greeting_html_escaped

**File(s)**: `src/nmg_sdlc_smoke/greet.py`, `src/nmg_sdlc_smoke/__init__.py`, `README.md`
**Type**: Modify
**Depends**: none
**Acceptance**:
- In `greet.py`, add `import html` after `import hashlib`, and add `greeting_html_escaped(name: str) -> str` returning `html.escape(greet(name))`, immediately after `greeting_url_encoded` (AC1, AC2, AC3, FR1, FR2).
- In `__init__.py`:
  - add the self-aliased import `from .greet import greeting_html_escaped as greeting_html_escaped` immediately after the `greeting_has_underscore` import;
  - add the `__all__` entry `"greeting_html_escaped"` immediately after `"greeting_has_underscore"`;
  - remove no existing export (AC4, FR3, FR5).
- In README `## Library`:
  - add `greeting_html_escaped,` after `greeting_has_underscore,` in the import list;
  - add the `greeting_html_escaped("<Ada & Bo>")  # "Hello, &lt;Ada &amp; Bo&gt;"` example after the `greeting_url_encoded("Ada")` example;
  - add the exact `greeting_html_escaped` prose line from design.md after the `greeting_url_encoded` prose line (AC4, FR4).

### T002: Cover the helper with pytest unit tests

**File(s)**: `tests/test_greet.py`
**Type**: Modify
**Depends**: T001
**Acceptance**:
- Add `import html` to the module imports and `greeting_html_escaped` to the package-root import list after `greeting_has_underscore`.
- Parameterize `"Ada"`, `"Zoë"` (precomposed U+00EB), `"<Ada & Bo>"`, and `O'Brien "Jr"` with their exact results from AC1 and AC2. For each, assert `type(result) is str`, the exact value, and equality with `html.escape(greet(name))` (AC1, AC2).
- Parameterize `""`, `" \t"`, `None`, and `42`. For each, assert `pytest.raises(ValueError, match="^name must not be blank$")` (AC3).
- Assert `"greeting_html_escaped" in nmg_sdlc_smoke.__all__` and `nmg_sdlc_smoke.greeting_html_escaped("<Ada & Bo>") == "Hello, &lt;Ada &amp; Bo&gt;"` (AC4).
- Run `python -m pytest tests/test_greet.py -k greeting_html_escaped`.

### T003: Exercise four AC-linked pytest-bdd scenarios

**File(s)**: `tests/features/add_greeting_html_escaped_library_helper.feature`, `tests/features/steps/test_greeting_html_escaped_steps.py`
**Type**: Create
**Depends**: T001
**Acceptance**:
- Copy the four tagged scenarios from this spec's `feature.gherkin` into the executable `.feature`, without frontmatter or source comments.
- Implement deterministic steps with `scenarios("../add_greeting_html_escaped_library_helper.feature")` and public `nmg_sdlc_smoke` imports. Follow `tests/features/steps/test_greeting_url_encoded_steps.py` (AC1–AC4).
- Assert:
  - `Hello, Ada` for `"Ada"` and `Hello, Zoë` for `"Zoë"`, in that order, each of type `str` (AC1);
  - `Hello, &lt;Ada &amp; Bo&gt;` for `"<Ada & Bo>"` and `Hello, O&#x27;Brien &quot;Jr&quot;` for `O'Brien "Jr"`, each equal to `html.escape(greet(name))` (AC2);
  - `ValueError` with exact message `name must not be blank` for `""`, `" \t"`, `None`, and `42` (AC3);
  - the README example and unchanged CLI (AC4), as follows:
    - read the first fenced `python` block of `README.md`, resolved from `Path(__file__).resolve().parents[3]`;
    - append `print(greeting_html_escaped("<Ada & Bo>"))` and run the result with `sys.executable -c`;
    - the run gives `(returncode, stdout, stderr) == (0, "Hello, &lt;Ada &amp; Bo&gt;\n", "")`;
    - `"greeting_html_escaped" in nmg_sdlc_smoke.__all__`, and every name previously in `__all__` (including `greeting_has_underscore`, `greeting_is_ascii`, and `greeting_url_encoded`) remains;
    - the exact `greeting_html_escaped` prose line from design.md is one of the lines of `README.md`;
    - `nmg_sdlc_smoke.cli.main(["Ada"])` returns `0` and writes exactly `Hello, Ada\n` to stdout.
- Run `python -m pytest tests/features/steps/test_greeting_html_escaped_steps.py`.

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #293 | 2026-11-08 | Initial feature tasks |
