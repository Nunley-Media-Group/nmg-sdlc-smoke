# Structure Steering

## Canonical Layout

```text
.
├── pyproject.toml
├── VERSION
├── src/
│   └── nmg_sdlc_smoke/
│       ├── __init__.py
│       ├── greet.py
│       └── cli.py
├── tests/
│   ├── test_greet.py
│   ├── test_cli.py
│   └── features/
│       ├── convert_smoke_repository_to_a_python_sdlc_host.feature
│       └── steps/test_greeting_steps.py
├── specs/
├── steering/
└── .github/workflows/python-ci.yml
```

## Responsibilities

- `src/nmg_sdlc_smoke/greet.py`: pure greeting and input validation.
- `src/nmg_sdlc_smoke/cli.py`: argument parsing, stdout/stderr behavior, and exit status.
- `src/nmg_sdlc_smoke/__init__.py`: minimal public API exports.
- `tests/test_*.py`: fast unit contracts.
- `tests/features/`: pytest-bdd scenarios for every approved acceptance criterion.
- `specs/{N}-{slug}/`: singular current issue contract with requirements, design, tasks, and feature.
- `steering/`: stable product, technology, and repository conventions.
- `VERSION`: 3.x version source consumed by `pyproject.toml`.

## Boundaries

The CLI may call the library; the library must not depend on the CLI, tests, GitHub Actions, or repository layout. Test-only dependencies stay in the `dev` extra. Avoid utility modules, service layers, compatibility aliases, generated source, and extra frameworks unless an approved spec creates a real need.

The current working tree is a Python SDLC smoke host, not an Oh My Pi plugin. Superseded plugin files belong only in Git history.
