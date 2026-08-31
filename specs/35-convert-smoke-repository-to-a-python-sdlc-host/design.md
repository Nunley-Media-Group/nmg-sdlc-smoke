# Design: Convert smoke repository to a Python SDLC host

**Issue**: #35
**Date**: 2026-08-31
**Status**: Approved
**Author**: NMG
---

## Overview

Replace the copied nmg-sdlc Oh My Pi plugin working tree with a minimal installable Python 3.12+ distribution named `nmg-sdlc-smoke-python`. The only runtime behavior is `greet` plus console script `nmg-smoke`. Verification is pytest, pytest-bdd under `tests/features/`, Ruff, and GitHub Actions Python CI. Managed SDLC host contracts (LICENSE, 3.x VERSION, CHANGELOG history, contribution gate, issue form, AGENTS spec-context markers) stay. Copied plugin runtime is deleted; Git history remains the archive.

This is an owner-approved working-tree rewrite. The implementation PR uses the managed repository-rewrite exception because pre-cutover plugin files predate this host's singular issue/spec workflow. Delivery remains a 3.x minor (`VERSION` `3.14.0`). Requirements spec: `specs/35-convert-smoke-repository-to-a-python-sdlc-host/requirements.md`.

---

## Architecture

### Component Diagram

Reference `structure.md` after the steering rewrite in this issue. Target layout:

```
┌──────────────────────────────────────────────────────────┐
│                    Presentation Layer                      │
│  console script nmg-smoke → nmg_sdlc_smoke.cli:main        │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    Business Logic Layer                    │
│  nmg_sdlc_smoke.greet.greet(name: str) -> str              │
└───────────────────────────┬──────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                    External Layer                          │
│  stdlib argparse / stdout / stderr / process exit code     │
└──────────────────────────────────────────────────────────┘
```

No database, HTTP, or UI.

### Data Flow

```
1. Caller imports greet or invokes nmg-smoke <name>
2. CLI parses a single positional name (argparse)
3. greet validates name
4. Valid: return/print "Hello, {name}"
5. Invalid: raise ValueError("name must not be blank"); CLI returns 1 with no stdout greeting
```

---

## API / Interface Changes

### New Endpoints / Methods

| Endpoint / Method | Type | Auth | Purpose |
|-------------------|------|------|---------|
| `nmg_sdlc_smoke.greet.greet(name: str) -> str` | function | No | Greeting library |
| `nmg_sdlc_smoke.cli.main(argv: list[str] \| None = None) -> int` | function | No | CLI entry |
| `nmg-smoke` | console script | No | Installed command |

### Request / Response Schemas

#### greet

**Input:** `name: str`

**Output (success):** `str` exactly `Hello, {name}` (example: `"Ada"` → `"Hello, Ada"`)

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| `ValueError("name must not be blank")` | `name` is not a `str`, or `name.strip() == ""` |

#### nmg-smoke

**Input:** argv positional `name`

**Output (success):** stdout bytes UTF-8 `Hello, Ada\n` for argument `Ada`; exit 0

**Errors:**

| Code / Type | Condition |
|-------------|-----------|
| exit `1` | `ValueError` from `greet`; stdout has no greeting |
| argparse non-zero | missing positional; usage on stderr; no greeting |

---

## Database / Storage Changes

### Schema Changes

None. No database.

### Migration Plan

Working-tree rewrite, not a data migration. Delete copied plugin files; add Python package files. Git history is the archive.

### Data Migration

None.

---

## State Management

None. `greet` is a pure function. CLI is a single invocation with no persistent state.

---

## UI Components

None. CLI only.

---

## Alternatives Considered

| Option | Description | Pros | Cons | Decision |
|--------|-------------|------|------|----------|
| **A: Keep plugin and add Python beside it** | Dual runtime | Less deletion | Fails AC5/AC6 clean cutover | Rejected — issue requires plugin runtime gone |
| **B: setuptools src layout + pytest-bdd + Ruff** | Minimal production-shaped Python host | Matches ACs; boring toolchain | Not a product | **Selected** |
| **C: Poetry/Hatch-only app without src layout** | Different packaging | Fashionable | Extra tool; issue names src layout | Rejected |

---

## Security Considerations

- [x] **Authentication**: None
- [x] **Authorization**: None
- [x] **Input Validation**: `greet` rejects blank/whitespace-only/non-str names
- [x] **Data Sanitization**: Name is interpolated only into the greeting string; not passed to a shell
- [x] **Sensitive Data**: None

---

## Performance Considerations

- [x] **Caching**: None
- [x] **Pagination**: None
- [x] **Lazy Loading**: None
- [x] **Indexing**: None

---

## Testing Strategy

| Layer | Type | Coverage |
|-------|------|----------|
| Business Logic | Unit `tests/test_greet.py` | happy path, blank, whitespace, non-str |
| CLI | Unit `tests/test_cli.py` | exit 0 + stdout, exit 1 + no greeting |
| Feature | pytest-bdd `tests/features/` | AC1–AC7 |
| Lint | Ruff | `src` and `tests` |
| CI | GitHub Actions Python 3.12 | install, pytest, pytest tests/features, ruff |

---

## Packaging

`pyproject.toml` (normative):

```toml
[build-system]
requires = ["setuptools>=69", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "nmg-sdlc-smoke-python"
dynamic = ["version"]
description = "Disposable Python SDLC smoke host"
readme = "README.md"
license = { file = "LICENSE" }
requires-python = ">=3.12"
authors = [{ name = "Nunley Media Group LLC" }]

[project.optional-dependencies]
dev = ["pytest>=8", "pytest-bdd>=8", "ruff>=0.6"]

[project.scripts]
nmg-smoke = "nmg_sdlc_smoke.cli:main"

[tool.setuptools.dynamic]
version = {file = "VERSION"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.ruff]
target-version = "py312"
src = ["src", "tests"]
```

Root `VERSION` after implementation is the two-line file `3.14.0` plus a single trailing LF.

`.gitignore` must include `__pycache__/`, `*.py[cod]`, `.pytest_cache/`, `.ruff_cache/`, `*.egg-info/`, `dist/`, `build/`, `.venv/`, and keep `.omp/sdlc/`. Remove Node `node_modules/` entries.

---

## Cutover inventory

Delete from the working tree (non-exhaustive names that must be gone; directories mean the whole tree):

- `workflows/`
- `agents/`
- `commands/`
- `scripts/` (Node/Jest)
- `package.json`
- `src/extension.ts`, `src/sdlc-commands.mjs`, `src/sdlc-workflows.mjs`
- all `specs/{N}-*` except `specs/35-convert-smoke-repository-to-a-python-sdlc-host/`
- plugin `references/` except the three rewrite-contract files listed below
- `.github/workflows/nmg-sdlc-verify.yml`
- `.github/workflows/skill-inventory-audit.yml`
- `.github/workflows/sync-marketplace-pointer.yml`
- `LIVE_SMOKE_A.txt`, `LIVE_SMOKE_B.txt`, `LIVE_SMOKE_C.txt`, `LIVE_SMOKE_D.txt`, `LIVE_SMOKE_259_A.txt`, `LIVE_SMOKE_259_B.txt`, `LIVE_SMOKE_214_C.txt`, `EXECUTE_SMOKE.md`

Preserve:

- `LICENSE` (MIT, Nunley Media Group LLC) byte-for-byte
- `CHANGELOG.md` history (do not wipe released headings)
- `.github/workflows/nmg-sdlc-contribution-gate.yml` version-6 evaluator; add only a comment that this host is a Python SDLC smoke consumer so the path changes
- `.github/ISSUE_TEMPLATE/nmg-sdlc-ready-issue.yml`
- AGENTS.md `<!-- nmg-sdlc-managed: spec-context -->` … `<!-- /nmg-sdlc-managed -->` markers and the spec-context rules inside them
- CONTRIBUTING.md managed contribution-workflow contract (issue/spec evidence, docs-only, repository-rewrite, spec-only write-spec table)

Rewrite current-product prose in `README.md`, `CONTRIBUTING.md` project context, `AGENTS.md` overview/structure/version sections, `steering/product.md`, `steering/tech.md`, `steering/structure.md`. Replace `steering/retrospective.md` with a short note that this host is the Python SDLC smoke project and plugin retrospectives live in Git. Set `steering/retrospective-state.json` to `{"version": 1, "specs": {}}`.

Rewrite `references/rewrite-contract.json`, `references/rewrite-contract.md`, and `references/rewrite-verification.md` so they document this Python host cutover (runtime Python 3.12+, exception `repository-rewrite`, capabilities `greet`, `nmg-smoke`, pytest/pytest-bdd, Ruff, Python CI). They must remain present because the contribution gate requires those paths on the rewrite PR.

---

## Implementation PR contract

Title: `feat!: convert smoke repository to a Python SDLC host`

Body must include:

- `Closes #35`
- `**Issue**: #35`
- `SDLC-Exception: repository-rewrite — Pre-cutover plugin files predate this host's singular issue/spec workflow.`
- steering alignment naming `steering/product.md`, `steering/tech.md`, `steering/structure.md`
- verification commands and outcomes (`python -m pytest`, `python -m pytest tests/features`, `python -m ruff check .`)

Changed paths must include every rewrite-required path listed in the contribution gate.

---

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Rewrite exception misses a required path | Med | High | Tasks list every required path; VERSION bump and package.json deletion are explicit |
| Plugin specs left in `specs/` | Med | High | Delete every spec dir except `#35` |
| Contribution gate evaluator accidentally edited | Low | High | Comment-only change; keep version 6 predicates |

---

## Open Questions

None.

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #35 | 2026-08-31 | Initial feature spec |

---

## Validation Checklist

Before moving to TASKS phase:

- [x] Architecture follows the post-cutover Python src layout
- [x] All API/interface changes documented with schemas
- [x] Database/storage changes planned with migrations
- [x] State management approach is clear
- [x] UI components and hierarchy defined
- [x] Security considerations addressed
- [x] Performance impact analyzed
- [x] Testing strategy defined
- [x] Alternatives were considered and documented
- [x] Risks identified with mitigations
