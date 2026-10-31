/**
 * Порядок и подписи лабораторных работ — то, что видят студенты в навигации и списке.
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { labOrder, labKind } from '../src/lib/labs.mjs';

test('labOrder: номер работы важнее номера в имени файла', () => {
  assert.equal(labOrder({ id: '02-laboratornaya-2', data: { number: 2 } }), 2);
  assert.equal(labOrder({ id: '03-park', data: {} }), 3);
  assert.equal(labOrder({ id: 'bez-nomera', data: {} }), 0);
});

test('labKind: короткая надпись для списка', () => {
  assert.equal(labKind({ data: { number: 2 } }), 'Лабораторная 2');
  assert.equal(labKind({ data: {} }), 'Лабораторная');
});
