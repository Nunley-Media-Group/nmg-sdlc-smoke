# Contributing

## Project Context

`nmg-sdlc-smoke-python` is a minimal Python SDLC smoke host. Contributors should preserve its setuptools `src` layout, Python 3.12+ support, pytest and pytest-bdd verification, Ruff checks, and the `VERSION` source synchronized dynamically with `pyproject.toml`.

Before changing code, read `steering/product.md`, `steering/tech.md`, and `steering/structure.md`. Start from a GitHub issue with an approved singular spec under `specs/{N}-{slug}/`. Git history is the archive for superseded behavior.

## Implementation and Verification

Implement only approved spec tasks. Keep the library pure and the CLI thin. Run:

```console
python -m pytest
python -m pytest tests/features
python -m ruff check .
```

Record commands and outcomes in the pull request. Keep paths cross-platform and do not add machine-specific absolute paths.

## nmg-sdlc Contribution Workflow

Before requesting review, confirm the pull request is ready for the managed nmg-sdlc contribution gate:

- Link the GitHub issue in the PR body or spec frontmatter, using `Closes #N`, `Fixes #N`, or `**Issue**: #N`.
- Link or update the relevant `specs/{N}-{slug}/` artifacts, including `requirements.md`, `design.md`, `tasks.md`, and `feature.gherkin` (or the matching ADR) when generated.
- Explain steering alignment against `steering/product.md`, `steering/tech.md`, and `steering/structure.md`.
- Summarize verification evidence from tests, exercise runs, verification results, or a committed `verification-report.md`.
- Include reviewer context for known gaps, intentionally deferred work, or follow-up issues.

If the contribution gate fails, fix the missing evidence category instead of bypassing the workflow. Missing issue, spec, steering, verification, or guide evidence should be remediated in the PR body or committed artifacts before re-running the gate.

### Evidence Consistency

The contribution gate evaluates a connected evidence graph rather than accepting unrelated keywords:

- **Issue/spec identity**: reference the current issue explicitly, such as `Closes #143`, and ensure the selected spec directory names that same issue in singular `**Issue**: #143` or its current body. Quoted examples, HTML comments, historical sections, and unrelated specs do not correlate.
- **Exact path evidence**: name an affected path exactly when a task or verification entry covers one file, such as `src/nmg_sdlc_smoke/greet.py`.
- **Directory-prefix evidence**: use an explicit directory ending in `/`, such as `tests/features/`, when the evidence covers that directory. A basename alone is insufficient.
- **Path-specific behavior evidence**: use a structured entry such as `Behavior for src/nmg_sdlc_smoke/greet.py: rejects blank names` when behavior is more useful than a file-operation description.
- **Command and outcome**: record both the command and result, for example `` `python -m pytest` — passed (19 tests) ``. Generic statements such as “tests run” are not specific evidence.
- **Other accepted verification**: a non-empty `verification-report.md`, an `AC9: passed` result, or a changed path paired with `passed`, `failed`, `verified`, or `covered` can also provide concrete evidence.

Reduced-evidence modes are validated contracts, not bypasses:

| Mode | Declaration and validation | Reduced checks | Still required | Invalidating conditions |
|------|----------------------------|----------------|----------------|-------------------------|
| Documentation-only | `SDLC-Exception: docs-only — <non-empty reason>` and every change is project documentation | Spec correlation, relevant-path mapping, and specific verification | Current issue linkage, steering artifacts and alignment, guide discoverability, and all other checks | Source, workflow, script, skill, template, shared reference, spec, ADR, or any other non-documentation path |
| Repository rewrite | `SDLC-Exception: repository-rewrite — <non-empty reason>`; PR title starts `feat!:`; `package.json`, `VERSION`, `README.md`, `CONTRIBUTING.md`, all steering files, the managed contribution gate, `references/rewrite-contract.{json,md}`, and `references/rewrite-verification.md` change | Current PR issue/spec identity only | Genuinely owned current spec archive, explicit rewrite contract, durable verification, steering alignment, exact changed-path mapping, specific verification, and guide discoverability | Missing contract path, non-breaking title, unmatched relevant path, missing steering, or missing verification |
| Spec-only write-spec | Title matches `^docs: approve spec for #(\d+)$`; that issue number appears in current PR text; every changed path is class `spec` under exactly one `specs/{N}-{slug}/` whose leading number is that issue | Steering alignment text and specific verification | Current issue linkage, spec correlation, steering artifacts, guide discoverability, and all other checks | Any non-spec path, title mismatch, multiple spec directories, or issue number mismatch |

The repository-rewrite exception exists for an owner-approved clean cutover where pre-cutover work predates the current singular issue/spec workflow. It must not be used for ordinary feature or bug delivery.

Remove an invalid exception or split invalidating implementation changes into a normally evidenced pull request. A marker, label, or rationale never overrides incompatible changed paths.
