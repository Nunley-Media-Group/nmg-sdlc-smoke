# Design: Add --help to publish-approved-spec

**Issue**: #3
**Date**: 2026-08-20
**Status**: Approved
**Author**: write-spec
---

## Overview

Add a first-token `--help` branch in `main()` of `scripts/publish-approved-spec.mjs`. Print the existing usage line as plain text and exit 0. Keep every other first-token path, including JSON `fail()` for unknown or missing commands, byte-compatible.

No new files. No skill, agent, or extension changes. Tests extend `scripts/__tests__/publish-approved-spec.test.mjs` using the existing `run()` spawn helper.

---

## Architecture

`main(argv = process.argv.slice(2))` already destructures `[command, ...rest]`. Insert the help branch immediately after that destructure and before the `prepare` check.

```
argv[0] === '--help'  →  stdout.write(USAGE + '\n'); return
argv[0] === 'prepare' | 'commit-push' | 'merge' | 'default-branch'  →  unchanged
else (including undefined, '-h', '--HELP', 'help')  →  fail('invalid_arguments', { detail: USAGE })
```

No storage, UI, or network changes.

---

## API / Interface Changes

### New first-token

| Token | Type | Auth | Purpose |
|-------|------|------|---------|
| `--help` | CLI first argument | No | Print usage text; exit 0 |

### Request / Response

**Input:** `node scripts/publish-approved-spec.mjs --help` (optional extra argv after `--help` ignored)

**Output (success):** plain text, not JSON:

```
Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...
```

Exit status 0. Do not call `ok()` or `fail()`.

**Unchanged failure (missing or unknown first token):** JSON line plus exit 1:

```json
{"ok":false,"reasonCode":"invalid_arguments","detail":"Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ..."}
```

---

## Implementation

In `scripts/publish-approved-spec.mjs`, immediately after `const SLUG_RE = ...`:

```js
const USAGE =
  'Usage: node scripts/publish-approved-spec.mjs <prepare|commit-push|merge|default-branch> ...';
```

Replace the `fail('invalid_arguments', { detail: 'Usage: ...' })` literal in `main` with `{ detail: USAGE }`.

In `main`, after `const [command, ...rest] = argv;`:

```js
  if (command === '--help') {
    process.stdout.write(`${USAGE}\n`);
    return;
  }
```

Do not export `main`. Do not treat `-h`. Do not parse `--help` from `rest`. Leave `prepare`/`commit-push`/`merge`/`default-branch` bodies untouched.

---

## Testing Strategy

| Layer | Type | Coverage |
|-------|------|----------|
| CLI dispatch | Jest spawn via existing `run()` | `--help` exit 0 + usage substring; `[]`, `['-h']`, `['nope']`, `['prepare', '--help']` remain `invalid_arguments` |
| Existing contract | Jest | All current prepare/commit-push/merge cases still pass |

Add tests to `scripts/__tests__/publish-approved-spec.test.mjs` inside `describe('publish-approved-spec')`. Use `run(os.tmpdir(), args)` for dispatch-only cases so they do not need a git repo.

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #3 | 2026-08-20 | Initial feature spec |
