# Design: Add public greeting_has_ampersand helper

**Issue**: #150
**Date**: 2026-09-24
**Status**: Approved
**Author**: NMG
**Related Spec**: specs/146-add-public-greeting-has-equal-helper/

## Overview

Follow the existing pure punctuation predicates: inspect the completed greeting once, inherit input validation from `greet`, and expose the typed helper at the package root. No new module, CLI path, or runtime dependency is needed.

## Architecture

Add `def greeting_has_ampersand(name: str) -> bool:` to `src/nmg_sdlc_smoke/greet.py` beside the other punctuation predicates, returning `"&" in greet(name)`. Add `from .greet import greeting_has_ampersand as greeting_has_ampersand` and `"greeting_has_ampersand"` to `__all__` in `src/nmg_sdlc_smoke/__init__.py` without removing existing names. In `README.md`'s Library section, add the public import, `greeting_has_ampersand("Ada&")  # True`, `greeting_has_ampersand("Ada")  # False`, and a literal-ASCII/validation explanation beside the existing equals-sign example. Add focused public-import tests to `tests/test_greet.py` and four AC-linked pytest-bdd scenarios to `tests/features/add_public_greeting_has_ampersand_helper.feature`, backed by `tests/features/steps/test_greeting_has_ampersand_steps.py`. For AC4, check every preexisting export listed in `__all__`: `greet`, `greet_many`, `greeting_bytes`, `greeting_casefold`, `greeting_ends_with_exclamation`, `greeting_ends_with_name`, `greeting_has_at_sign`, `greeting_has_colon`, `greeting_has_equal`, `greeting_has_hash`, `greeting_has_percent`, `greeting_has_plus`, `greeting_has_question_mark`, `greeting_has_semicolon`, `greeting_is_ascii`, `greeting_length`, `greeting_starts_with_hello`, and `greeting_word_count`. Use the existing pytest-bdd step module's `sysconfig.get_path("scripts")` and `nmg-smoke`/`nmg-smoke.exe` lookup for the installed CLI.

## API / Interface Changes

| Interface | Input | Output / Error | Behavior |
|-----------|-------|----------------|----------|
| `nmg_sdlc_smoke.greeting_has_ampersand(name: str) -> bool` | Valid nonblank string name | Python `True` or `False`; invalid input raises `ValueError("name must not be blank")` | Return `True` only when the complete greeting contains ASCII `&`; fullwidth `＆` does not match. |

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #150 | 2026-09-24 | Initial feature design |
