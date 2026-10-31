/**
 * Порядок и подписи руководств — то, что видят студенты в навигации и списке.
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { guideOrder, guideKind } from '../src/lib/guides.mjs';

test('guideOrder: поле order важнее номера в имени файла', () => {
  assert.equal(guideOrder({ id: 'laboratornaya-2', data: { order: 1 } }), 1);
  assert.equal(guideOrder({ id: '02-laba-3', data: {} }), 2);
  assert.equal(guideOrder({ id: 'bez-nomera', data: {} }), 0);
});

test('guideKind: короткая надпись для списка', () => {
  assert.equal(guideKind({ data: { seminar: 4 } }), 'Семинар 4');
  assert.equal(guideKind({ data: {} }), 'Руководство');
});
