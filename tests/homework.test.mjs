/**
 * Порядок и подписи заданий курса — то, что видят студенты в навигации и списках.
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { homeworkOrder, homeworkLabel, homeworkKind } from '../src/lib/homework.mjs';

test('homeworkOrder: номер из имени файла (01, 02, …)', () => {
  assert.equal(homeworkOrder({ id: '01-process-8-shagov' }), 1);
  assert.equal(homeworkOrder({ id: '10-model-sredy' }), 10);
  assert.equal(homeworkOrder({ id: 'bez-nomera' }), 0);
});

test('homeworkLabel: лекция > семинар > тема > название', () => {
  assert.equal(homeworkLabel({ data: { lecture: 4 } }), 'ДЗ по лекции 4');
  assert.equal(homeworkLabel({ data: { seminar: 2 } }), 'ДЗ к семинару 2');
  assert.equal(homeworkLabel({ data: { topic: 3 } }), 'ДЗ по теме 3');
  assert.equal(homeworkLabel({ data: { title: 'Своё название' } }), 'Своё название');
  assert.equal(
    homeworkLabel({ data: { lecture: 1, seminar: 2, topic: 3, title: 'Всё сразу' } }),
    'ДЗ по лекции 1'
  );
});

test('homeworkKind: короткая надпись для списков', () => {
  assert.equal(homeworkKind({ data: { lecture: 4 } }), 'Лекция 4');
  assert.equal(homeworkKind({ data: { seminar: 2 } }), 'К семинару 2');
  assert.equal(homeworkKind({ data: { topic: 3 } }), 'К теме 3');
  assert.equal(homeworkKind({ data: {} }), 'Задание');
});
