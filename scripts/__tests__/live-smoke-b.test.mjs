import { expect, test } from '@jest/globals';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const repoRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

test('LIVE_SMOKE_B marker has exact bytes', () => {
  const actual = fs.readFileSync(path.join(repoRoot, 'LIVE_SMOKE_B.txt'));
  expect(actual).toEqual(Buffer.from('smoke-b-213\n', 'utf8'));
});
