# Implementation verification: #123

**Issue**: #123
**Status**: Pending delivery

The public `greeting_has_question_mark` query detects a literal `?` in the completed greeting and delegates invalid-name validation to `greet`. Independent unit and pytest-bdd scenarios cover positive, negative, and invalid inputs. The CLI is unchanged.

## Checks

- Isolated editable install: `python -m pip install -e ".[dev]"` passed using Python 3.14.6.
- Focused check: `python -m pytest tests/test_greet.py tests/features/steps/test_greeting_has_question_mark_steps.py -q` passed (95 tests). pytest emitted third-party Gherkin deprecation warnings and unregistered `AC1`–`AC3` mark warnings.
- `python -m pytest -q`: 229 passed, 2 skipped; third-party Gherkin/pytest-bdd warnings and unregistered AC marks.
- `python -m pytest tests/features -q`: 86 passed, 2 skipped; same third-party and mark warnings.
- `python -m ruff check .`: all checks passed.

## Lifecycle boundary

No exact-head merged PR or issue closure is asserted here. Registered verification, release/version/changelog update, PR merge, and issue closure belong to subsequent normal delivery; those outcomes must be recorded only after observed evidence exists.
