/**
 * Единая логика id заголовков: rehype-плагин, содержание темы/занятия и якоря
 * вопросов обязаны давать одинаковые id на одной странице.
 */
import test from 'node:test';
import assert from 'node:assert/strict';

import { createIdNamer, bodyHeadings } from '../src/lib/headings.mjs';

test('createIdNamer: повторам добавляется суффикс -1, -2', () => {
  const namer = createIdNamer();
  assert.equal(namer.claim('Введение'), 'введение');
  assert.equal(namer.claim('Введение'), 'введение-1');
  assert.equal(namer.claim('Введение'), 'введение-2');
  assert.equal(namer.claim('Другое'), 'другое');
});

test('createIdNamer: пустой текст — fallback, повтор учитывается', () => {
  const namer = createIdNamer();
  assert.equal(namer.claim('!!!', 'vopros'), 'vopros');
  assert.equal(namer.claim('?!?', 'vopros'), 'vopros-1');
});

test('createIdNamer: разные экземпляры нумеруют независимо', () => {
  const a = createIdNamer();
  const b = createIdNamer();
  assert.equal(a.claim('Ответ'), 'ответ');
  assert.equal(b.claim('Ответ'), 'ответ');
});

test('bodyHeadings: только ## и ###, ** срезается, повторы получают суффикс', () => {
  const body = [
    '# Вступление — не берём',
    '## Первый раздел',
    '### Подраздел',
    '#### Вложенный — не берём',
    '## **Жирный** заголовок',
    '',
    '## Первый раздел',
  ].join('\n');
  assert.deepEqual(bodyHeadings(body), [
    { text: 'Первый раздел', id: 'первый-раздел', level: 1 },
    { text: 'Подраздел', id: 'подраздел', level: 2 },
    { text: 'Жирный заголовок', id: 'жирный-заголовок', level: 1 },
    { text: 'Первый раздел', id: 'первый-раздел-1', level: 1 },
  ]);
});

test('bodyHeadings: без тела и без заголовков — пустой список', () => {
  assert.deepEqual(bodyHeadings(null), []);
  assert.deepEqual(bodyHeadings('Текст без заголовков'), []);
});

test('общий namer: якоря вопросов продолжают нумерацию заголовков', () => {
  const namer = createIdNamer();
  const headings = bodyHeadings('## Доход и дисконтирование', namer);
  assert.equal(headings[0].id, 'доход-и-дисконтирование');
  // вопрос с тем же текстом не должен получить тот же id
  assert.equal(namer.claim('Доход и дисконтирование', 'vopros'), 'доход-и-дисконтирование-1');
});
