import { expect, test } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('LIVE_SMOKE_A marker has exact bytes', () => {
  const actual = fs.readFileSync(path.join(repoRoot, 'LIVE_SMOKE_A.txt'));
  expect(actual).toEqual(Buffer.from('smoke-a-213\n', 'utf8'));
});
