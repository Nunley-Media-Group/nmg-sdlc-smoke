# Design: Add second serial lifecycle smoke marker

**Issue**: #12
**Date**: 2026-08-24
**Status**: Approved
**Author**: NMG

---

## Overview

Issue #12 adds a repository-only completion contract for the second serial lifecycle item. A new root regular file supplies the byte-stable marker, one README sentence exposes the exact contract publicly, and one Jest ESM test enforces the complete bytes on every `cd scripts && npm test` run.

The implementation does not enter `src/`, workflow bundles, agents, extension registration, package configuration, or GitHub Actions. It reuses the existing root-resolution convention in `scripts/__tests__/` and the exact-byte `Buffer` comparison pattern documented by the adjacent lifecycle-marker spec, while keeping the B marker independent.

---

## File Contract

| Path | Change | Contract |
|------|--------|----------|
| `LIVE_SMOKE_B.txt` | Create | Entire file is the UTF-8 byte sequence `smoke-b-213\n`: token bytes followed by one LF and nothing else. |
| `README.md` | Modify | Under `## Verification Gates`, append the exact sentence defined below and preserve unrelated prose. |
| `scripts/__tests__/live-smoke-b.test.mjs` | Create | Resolve repository root from `import.meta.url`, read the marker as a `Buffer`, and compare it with the canonical `Buffer`. |

---

## Exact-Byte Test Contract

Implement `scripts/__tests__/live-smoke-b.test.mjs` as:

```javascript
import { expect, test } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('LIVE_SMOKE_B marker has exact bytes', () => {
  const actual = fs.readFileSync(path.join(repoRoot, 'LIVE_SMOKE_B.txt'));
  expect(actual).toEqual(Buffer.from('smoke-b-213\n', 'utf8'));
});
```

Omitting the encoding argument from `readFileSync` is deliberate: Jest compares raw bytes rather than normalized text. A missing file raises `ENOENT` inside the test; a changed token, missing newline, extra newline, BOM, carriage return, or any other byte difference fails `toEqual`. The test reads only a tracked local file and has no network, clock, or environment dependency.

---

## Documentation Contract

Append this exact sentence after the existing paragraph under README `## Verification Gates`:

> The root [`LIVE_SMOKE_B.txt`](LIVE_SMOKE_B.txt) second serial lifecycle marker contains exactly `smoke-b-213` followed by one final newline.

Do not modify any other README section.

---

## API and Runtime Impact

There are no new endpoints, commands, configuration keys, schemas, state transitions, UI components, runtime dependencies, or production code paths. The new test uses only Node built-ins plus the existing `@jest/globals` dependency.

---

## Testing Strategy

| Layer | Command or evidence | Required result |
|-------|---------------------|-----------------|
| Exact artifact | Read root `LIVE_SMOKE_B.txt` as bytes | Equals `Buffer.from('smoke-b-213\n', 'utf8')`. |
| Documentation | Read README `## Verification Gates` | Contains the exact sentence above, including the filename, token, and final-newline contract. |
| Focused positive contract | From `scripts/`, run `npm test -- --runTestsByPath __tests__/live-smoke-b.test.mjs` with the canonical marker | Exit 0. |
| Focused drift contract | Temporarily exercise the focused test with the marker missing, changed, lacking its LF, and containing an extra LF; restore canonical bytes after each probe | Every drift probe exits non-zero because the exact-byte assertion fails. |
| Repository regression | From `scripts/`, run `npm test` after restoring canonical bytes | Existing and new Jest ESM contract tests pass. |
| BDD traceability | Compare `requirements.md` AC1-AC4 with `feature.gherkin` `@SCN001`-`@SCN004` | One stable scenario maps to each acceptance criterion. |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #12 | 2026-08-24 | Initial feature spec |
