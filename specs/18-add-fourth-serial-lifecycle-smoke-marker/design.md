# Design: Add fourth serial lifecycle smoke marker

**Issue**: #18
**Date**: 2026-08-25
**Status**: Approved
**Author**: NMG

---

## Overview

Issue #18 adds a repository-only completion contract for the fourth serial lifecycle item. A new root regular file supplies the byte-stable marker, one README sentence exposes the exact contract publicly, and one Jest ESM test enforces both the complete marker bytes and the README mention on every `cd scripts && npm test` run.

The implementation does not enter `src/`, workflow bundles, agents, extension registration, package configuration, or GitHub Actions. It reuses the existing root-resolution convention in `scripts/__tests__/`. Unlike `live-smoke-a.test.mjs` and `live-smoke-b.test.mjs`, which assert marker bytes only, this test also reads `README.md` as UTF-8 and requires the documentation sentence. The D marker stays independent of A, B, and C.

---

## File Contract

| Path | Change | Contract |
|------|--------|----------|
| `LIVE_SMOKE_D.txt` | Create | Entire file is the UTF-8 byte sequence `LIVE_SMOKE_D\n`: token bytes followed by one LF and nothing else. |
| `README.md` | Modify | Under `## Verification Gates`, append the exact sentence defined below after the existing lifecycle marker sentences and preserve unrelated prose. |
| `scripts/__tests__/live-smoke-d.test.mjs` | Create | Resolve repository root from `import.meta.url`, compare marker bytes to the canonical `Buffer`, and assert README contains the documentation sentence. |

---

## Exact-Byte And README Test Contract

Implement `scripts/__tests__/live-smoke-d.test.mjs` as:

```javascript
import { expect, test } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('LIVE_SMOKE_D marker has exact bytes and README mention', () => {
  const actual = fs.readFileSync(path.join(repoRoot, 'LIVE_SMOKE_D.txt'));
  expect(actual).toEqual(Buffer.from('LIVE_SMOKE_D\n', 'utf8'));

  const readme = fs.readFileSync(path.join(repoRoot, 'README.md'), 'utf8');
  expect(readme).toContain(
    'The root [`LIVE_SMOKE_D.txt`](LIVE_SMOKE_D.txt) fourth serial lifecycle smoke marker contains exactly `LIVE_SMOKE_D` followed by one final newline.'
  );
});
```

Omitting the encoding argument from the marker `readFileSync` is deliberate: Jest compares raw bytes rather than normalized text. A missing marker raises `ENOENT` inside the test; a changed token, missing newline, extra newline, BOM, carriage return, or any other byte difference fails `toEqual`. README is read as UTF-8 so the mention assertion is a string contains. The test reads only tracked local files and has no network, clock, or environment dependency.

Do not copy `live-smoke-a.test.mjs` or `live-smoke-b.test.mjs` unchanged: those files omit the README assertion required by AC3 and AC4.

---

## Documentation Contract

Append this exact sentence after the existing lifecycle marker sentences under README `## Verification Gates`:

> The root [`LIVE_SMOKE_D.txt`](LIVE_SMOKE_D.txt) fourth serial lifecycle smoke marker contains exactly `LIVE_SMOKE_D` followed by one final newline.

Do not modify any other README section. Do not edit any existing marker sentence.

---

## API and Runtime Impact

There are no new endpoints, commands, configuration keys, schemas, state transitions, UI components, runtime dependencies, or production code paths. The new test uses only Node built-ins plus the existing `@jest/globals` dependency.

---

## Testing Strategy

| Layer | Command or evidence | Required result |
|-------|---------------------|-----------------|
| Exact artifact | Read root `LIVE_SMOKE_D.txt` as bytes | Equals `Buffer.from('LIVE_SMOKE_D\n', 'utf8')`. |
| Documentation | Read README `## Verification Gates` | Contains the exact sentence above, including the filename link, fourth-serial description, token, and final-newline contract. |
| Focused positive contract | From `scripts/`, run `npm test -- --runTestsByPath __tests__/live-smoke-d.test.mjs` with the canonical marker and README sentence | Exit 0. |
| Focused drift contract | Temporarily exercise the focused test with the marker missing, changed, lacking its LF, containing an extra LF, and with canonical bytes but the D sentence removed from README; restore canonical files after each probe | Every drift probe exits non-zero. |
| Repository regression | From `scripts/`, run `npm test` after restoring canonical bytes and README | Existing and new Jest ESM contract tests pass. |
| BDD traceability | Compare `requirements.md` AC1-AC4 with `feature.gherkin` `@SCN001`-`@SCN004` | One stable scenario maps to each acceptance criterion. |

---

## Change History

| Issue | Date | Summary |
|-------|------|---------|
| #18 | 2026-08-25 | Initial feature spec |
| #18 | 2026-08-25 | Spec revised before delivery |
