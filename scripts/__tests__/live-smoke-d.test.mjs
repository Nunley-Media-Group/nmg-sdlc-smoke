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
