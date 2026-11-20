/**
 * Занятия на двух языках: пары файлов и ссылки на материалы.
 *
 * Правило: английская запись — та же имя-файла в подпапке en/ коллекции seminars.
 * Проверяем то, что легко сломать руками: пару с одинаковым номером занятия
 * и существование каждого файла, на который страница ссылается.
 */
import test from 'node:test';
import assert from 'node:assert/strict';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

import { seminarLang, seminarSlug, enSeminarId, ruSeminarId } from '../src/lib/seminars.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const seminarsDir = join(root, 'src/content/seminars');
const enDir = join(seminarsDir, 'en');
const publicDir = join(root, 'public');

const readFrontmatter = (path) => {
  const text = readFileSync(path, 'utf8');
  const match = text.match(/^---\n([\s\S]*?)\n---/);
  return match ? match[1] : '';
};

const number = (frontmatter) => {
  const match = frontmatter.match(/^number:\s*(\d+)/m);
  return match ? Number(match[1]) : null;
};

const hrefs = (frontmatter) =>
  [...frontmatter.matchAll(/href:\s*"?([^"\n]+)"?/g)]
    .map((match) => match[1].trim())
    .filter((href) => href.startsWith('/files/'));

test('seminarLang: английские записи живут в подпапке en/', () => {
  assert.equal(seminarLang('07-saper-4x4'), 'ru');
  assert.equal(seminarLang('en/07-saper-4x4'), 'en');
});

test('seminarSlug: адрес занятия одинаков в обоих языках', () => {
  assert.equal(seminarSlug('07-saper-4x4'), '07-saper-4x4');
  assert.equal(seminarSlug('en/07-saper-4x4'), '07-saper-4x4');
  assert.equal(ruSeminarId('en/07-saper-4x4'), '07-saper-4x4');
  assert.equal(enSeminarId('07-saper-4x4'), 'en/07-saper-4x4');
});

test('у каждого английского занятия есть русский двойник с тем же номером', () => {
  const files = existsSync(enDir) ? readdirSync(enDir).filter((name) => name.endsWith('.md')) : [];
  for (const name of files) {
    const ruPath = join(seminarsDir, name);
    assert.ok(existsSync(ruPath), `нет русского файла ${name}`);
    const ruNumber = number(readFrontmatter(ruPath));
    const enNumber = number(readFrontmatter(join(enDir, name)));
    assert.equal(enNumber, ruNumber, `номер занятия расходится: ${name}`);
  }
});

test('все ссылки на материалы занятия ведут в существующие файлы', () => {
  const files = [
    ...readdirSync(seminarsDir)
      .filter((name) => name.endsWith('.md') && !name.startsWith('_'))
      .map((name) => join(seminarsDir, name)),
    ...(existsSync(enDir)
      ? readdirSync(enDir)
          .filter((name) => name.endsWith('.md'))
          .map((name) => join(enDir, name))
      : []),
  ];
  for (const path of files) {
    for (const href of hrefs(readFrontmatter(path))) {
      const file = join(publicDir, href.replace(/^\//, ''));
      assert.ok(existsSync(file), `нет файла ${href} (страница ${path.replace(root + '/', '')})`);
    }
  }
});
