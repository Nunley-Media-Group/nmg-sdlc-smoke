# Design: Add LIVE_SMOKE_A lifecycle verification marker

**Issue**: #11
**Date**: 2026-08-24
**Status**: Approved
**Author**: NMG

---

## Overview

Issue #11 adds a repository-only lifecycle verification contract. A new root regular file supplies the byte-stable artifact, one README sentence exposes the contract publicly, and one Jest ESM test enforces the exact bytes on every `cd scripts && npm test` run.

The implementation does not enter `src/`, workflow bundles, agents, extension registration, package configuration, or GitHub Actions. It follows the existing root-marker precedent from `EXECUTE_SMOKE.md` while adding the stronger documentation and deterministic test coverage required by issue #11.

---

## File Contract

| Path | Change | Contract |
|------|--------|----------|
| `LIVE_SMOKE_A.txt` | Create | Entire file is the UTF-8 byte sequence `smoke-a-213\n`: token bytes followed by one LF and nothing else. |
| `README.md` | Modify | Under `## Verification Gates`, append the exact sentence defined below and preserve unrelated prose. |
| `scripts/__tests__/live-smoke-a.test.mjs` | Create | Resolve repository root from `import.meta.url`, read the marker as a `Buffer`, and compare it with the canonical `Buffer`. |

---

## Exact-Byte Test Contract

Implement `scripts/__tests__/live-smoke-a.test.mjs` as:

```javascript
import { expect, test } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('LIVE_SMOKE_A marker has exact bytes', () => {
  const actual = fs.readFileSync(path.join(repoRoot, 'LIVE_SMOKE_A.txt'));
  expect(actual).toEqual(Buffer.from('smoke-a-213\n', 'utf8'));
});
```

Omitting the encoding argument from `readFileSync` is deliberate: Jest compares raw bytes rather than normalized text. A missing file raises `ENOENT` inside the test, while a missing newline, extra newline, BOM, changed token, or any other byte difference fails `toEqual`.

---

## Documentation Contract

Append this exact sentence after the existing paragraph under README `## Verification Gates`:

> The root [`LIVE_SMOKE_A.txt`](LIVE_SMOKE_A.txt) lifecycle marker contains exactly `smoke-a-213` followed by one final newline.

Do not modify any other README section.

---

## API and Runtime Impact

There are no new endpoints, commands, configuration keys, schemas, state transitions, UI components, runtime dependencies, or production code paths. The new test uses only Node built-ins plus the existing `@jest/globals` dependency.

---

## Testing Strategy

| Layer | Command or evidence | Required result |
|-------|---------------------|-----------------|
| Exact artifact | Read root `LIVE_SMOKE_A.txt` as bytes | Equals `Buffer.from('smoke-a-213\n', 'utf8')`. |
| Focused contract | From `scripts/`, run `npm test -- --runTestsByPath __tests__/live-smoke-a.test.mjs` | Exit 0 with the canonical marker; exit non-zero if the marker is missing or any byte differs. |
| Repository regression | From `scripts/`, run `npm test` | Existing and new Jest ESM contract tests pass. |
| BDD traceability | Compare `requirements.md` AC1-AC3 with `feature.gherkin` `@SCN001`-`@SCN003` | One stable scenario maps to each acceptance criterion. |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #11 | 2026-08-24 | Initial feature spec |
