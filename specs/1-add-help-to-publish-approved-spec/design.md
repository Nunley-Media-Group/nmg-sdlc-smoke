# Design: Add --help to publish-approved-spec

**Issue**: #1
**Date**: 2026-08-20
**Status**: Approved
**Author**: Rich Nunley

---

## Overview

Add a first-argument `--help` branch in `main()` of `scripts/publish-approved-spec.mjs`. Today `main()` destructures `const [command, ...rest] = argv` and dispatches `prepare`, `commit-push`, `merge`, and `default-branch`; every other first token, including `--help`, calls `fail('invalid_arguments', { detail: USAGE })` which writes JSON `{ ok: false, reasonCode, ...extra }` and `process.exit(1)`.

The help path must not use `fail()` or `ok()`. Those helpers always emit a JSON object. Help writes the existing usage line as plain text on stdout and exits 0.

No new module, helper, or shared CLI parser. Other scripts already print `--help` and return 0 (`scripts/skill-inventory-audit.mjs`); do not import that parser. The publisher stays a first-token switch.

---

## Architecture

### Component Diagram

```
node scripts/publish-approved-spec.mjs <first> ...
        │
        ▼
   main(argv)
        │
        ├─ first === '--help'  → stdout USAGE + '\n' ; process.exit(0)
        ├─ first === 'prepare' → prepare(rest)
        ├─ first === 'commit-push' → commitPush(rest)
        ├─ first === 'merge' → mergeSpec(rest)
        ├─ first === 'default-branch' → defaultBranch()
        └─ else → fail('invalid_arguments', { detail: USAGE })
```

USAGE is the existing literal:

`Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...`

### Data Flow

```
1. Process starts; main() receives process.argv.slice(2)
2. If argv[0] === '--help' (exact string):
   a. process.stdout.write(USAGE + '\n')
   b. process.exit(0)
   c. Remaining argv tokens are ignored
3. Else existing command switch runs unchanged
```

---

## API / Interface Changes

### CLI

| First argument | stdout | exit |
|----------------|--------|------|
| `--help` | Plain text containing USAGE. Exact bytes: `Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...\n`. Not JSON. | 0 |
| `prepare` / `commit-push` / `merge` / `default-branch` | Unchanged JSON via `ok()` / `fail()` | Unchanged |
| Any other first token, including `-h`, empty, or missing | Unchanged JSON `{ ok: false, reasonCode: "invalid_arguments", detail: USAGE }` | 1 |

`--help` after a subcommand (`prepare --help`) is unchanged: `flag()` only reads `--issue` / `--name` / `--dir` and does not treat `--help` as usage. Do not add nested help.

Do not add `-h`. `-h` remains unrecognized and takes the invalid-arguments path.

Do not change the USAGE string in `fail('invalid_arguments', …)`.

---

## File Changes

| File | Type | Change |
|------|------|--------|
| `scripts/publish-approved-spec.mjs` | Modify | In `main()`, after `const [command, ...rest] = argv`, add `if (command === '--help') { process.stdout.write('Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...\n'); process.exit(0); }` before the four command checks. |
| `scripts/__tests__/publish-approved-spec.test.mjs` | Modify | Add cases for `--help` success and unrecognized first-argument failure. Keep existing prepare / commit-push / merge cases. |

No skill, README, or other-script edits.

---

## Alternatives Considered

| Option | Description | Decision |
|--------|-------------|----------|
| A: Reuse `fail()` / `ok()` | Keep JSON envelope | Rejected — AC1 forbids invalid-arguments JSON and wants a usage line, not `{ ok: true }` |
| B: Treat any argv token `--help` as help | `argv.includes('--help')` | Rejected — first argument only; nested flags out of scope |
| C: Also accept `-h` | Match other scripts | Rejected — issue Out of Scope |
| D: First-token `--help` prints USAGE and exits 0 | Minimal branch in `main()` | **Selected** |

---

## Testing Strategy

| Layer | Type | Coverage |
|-------|------|----------|
| `--help` | Jest spawn of the script | Exit 0; stdout equals USAGE + newline; stdout is not JSON |
| Unrecognized first arg | Jest spawn | Exit 1; last stdout line parses to `{ ok: false, reasonCode: 'invalid_arguments' }` and `detail` contains USAGE |
| Known subcommands | Existing Jest cases | prepare / commit-push / merge success and failure unchanged |

Reuse `run()` / `parse()` already in `scripts/__tests__/publish-approved-spec.test.mjs`. `--help` and unrecognized-first-arg cases do not need `makeRepo()` because `main()` returns before git.

---

## Open Questions

None.

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #1 | 2026-08-20 | Initial feature spec |
