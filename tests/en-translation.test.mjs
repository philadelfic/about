/**
 * Английские переводы курса: структура совпадает с русским оригиналом,
 * ссылки на файлы живые, кириллицы в тексте нет (кроме кодов групп).
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { checkPair, findPairs } from '../scripts/check-en-translation.mjs';

const pairs = findPairs();

test('пары «русский → английский» проходят проверку структуры', () => {
  assert.ok(pairs.length > 0, 'переводов нет вовсе');
  for (const [ruPath, enPath] of pairs) {
    const problems = checkPair(ruPath, enPath);
    assert.deepEqual(problems, [], `${enPath}: ${problems.join('; ')}`);
  }
});
