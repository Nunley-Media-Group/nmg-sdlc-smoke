# Design: Add public greeting_has_equal helper

**Issue**: #146
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG

## Overview

Follow the existing punctuation predicates: query the completed greeting once, delegate input validation to `greet`, and expose the typed helper at the package root. No new module, CLI path, or runtime dependency is needed.

## Architecture

Add `def greeting_has_equal(name: str) -> bool:` beside `greeting_has_hash` in `src/nmg_sdlc_smoke/greet.py`, returning `"=" in greet(name)`. Add `from .greet import greeting_has_equal as greeting_has_equal` and `"greeting_has_equal"` to `__all__` in `src/nmg_sdlc_smoke/__init__.py`, preserving all existing entries. In `README.md`'s Library section, add the public import, `greeting_has_equal("Ada=")  # True`, `greeting_has_equal("Ada")  # False`, and a one-sentence literal-ASCII/validation explanation next to the existing hash example. Focused tests belong in `tests/test_greet.py`; implement four independently tagged pytest-bdd scenarios in `tests/features/add_public_greeting_has_equal_helper.feature` with steps in `tests/features/steps/test_greeting_has_equal_steps.py`. For AC4, compare the existing public names currently listed in `src/nmg_sdlc_smoke/__init__.py` (`greet`, `greet_many`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_at_sign`, `greeting_has_colon`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_is_ascii`, `greeting_length`, `greeting_starts_with_hello`, `greeting_word_count`) against importable package attributes; reuse the installed-script lookup pattern from `tests/features/steps/test_greeting_has_hash_steps.py` to exercise the real CLI.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_equal(name: str) -> bool` | Valid nonblank string name | Python `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Return `True` only when the complete greeting contains ASCII `=`; visually similar Unicode punctuation is not a match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #146 | 2026-09-24 | Initial feature design |
