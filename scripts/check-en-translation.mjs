#!/usr/bin/env node
/**
 * Проверка английского перевода записи курса против русского оригинала.
 *
 * Запуск: node scripts/check-en-translation.mjs [путь-ru:путь-en ...]
 * Без аргументов проверяет все пары, которые уже есть в репозитории.
 *
 * Что сверяем (структура, а не смысл):
 *   * тот же набор ключей frontmatter;
 *   * то же количество элементов в списках (covered, tasks, quiz, qa, terms, materials,
 *     groups, rows, lecture, options, sections);
 *   * то же количество заголовков ## и ###, блоков $$;
 *   * тот же набор ссылок на файлы (/files/...);
 *   * в английском тексте нет кириллицы, кроме кодов групп и значений схемы.
 */
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { dirname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const contentDir = join(root, 'src/content');

const ALLOWED_CYRILLIC = [/М80-\d{3}СВ-\d{2}/g, /зачёт|незачёт/g];

const readParts = (path) => {
  const text = readFileSync(path, 'utf8');
  const match = text.match(/^---\n([\s\S]*?)\n---\n?([\s\S]*)$/);
  if (!match) throw new Error(`нет frontmatter: ${path}`);
  return { frontmatter: match[1], body: match[2] };
};

const topKeys = (yaml) =>
  yaml
    .split('\n')
    .filter((line) => /^[a-zA-Z_]+:/.test(line))
    .map((line) => line.split(':')[0]);

/** Элементы списка под ключом верхнего уровня (строки «  - » или «  имя:»). */
const countItems = (yaml, key) => {
  const lines = yaml.split('\n');
  const start = lines.findIndex((line) => line.startsWith(`${key}:`));
  if (start === -1) return 0;
  let count = 0;
  for (let i = start + 1; i < lines.length; i += 1) {
    const line = lines[i];
    if (/^[a-zA-Z_]+:/.test(line)) break;
    if (/^ {2}- /.test(line) || /^ {2}\w+:/.test(line)) count += 1;
  }
  return count;
};

const countHeadings = (body, hashes) => (body.match(new RegExp(`^${hashes} `, 'gm')) || []).length;
const countBlocks = (body) => (body.match(/^\$\$$/gm) || []).length;
const fileLinks = (text) =>
  [...new Set([...text.matchAll(/\/files\/[^\s)"']+/g)].map((m) => m[0]))].sort();

const stripAllowed = (text) => {
  let out = text;
  for (const re of ALLOWED_CYRILLIC) out = out.replace(re, '');
  // Якоря (#цикл-агент-среда) ведут на русские страницы: их id русские, переводить нельзя.
  out = out.replace(/#[^\s"')]+/g, '');
  return out;
};

const cyrillic = (text) => (stripAllowed(text).match(/[А-Яа-яЁё]/g) || []).length;

export function checkPair(ruPath, enPath) {
  const problems = [];
  const ru = readParts(ruPath);
  const en = readParts(enPath);

  const ruKeys = topKeys(ru.frontmatter).join(',');
  const enKeys = topKeys(en.frontmatter).join(',');
  if (ruKeys !== enKeys) problems.push(`ключи frontmatter: ${ruKeys} ≠ ${enKeys}`);

  for (const key of new Set(topKeys(ru.frontmatter))) {
    const a = countItems(ru.frontmatter, key);
    const b = countItems(en.frontmatter, key);
    if (a !== b) problems.push(`${key}: элементов ${a} ≠ ${b}`);
  }

  for (const hashes of ['##', '###']) {
    const a = countHeadings(ru.body, hashes);
    const b = countHeadings(en.body, hashes);
    if (a !== b) problems.push(`заголовков ${hashes}: ${a} ≠ ${b}`);
  }

  const blocksA = countBlocks(ru.body);
  const blocksB = countBlocks(en.body);
  if (blocksA !== blocksB) problems.push(`блоков $$: ${blocksA} ≠ ${blocksB}`);

  // Материалов в переводе столько же, сколько в оригинале, и все они существуют на диске.
  // Совпадение адресов не требуем: у части материалов есть переведённый файл в en/.
  const linksA = fileLinks(ru.frontmatter + ru.body);
  const linksB = fileLinks(en.frontmatter + en.body);
  if (linksA.length !== linksB.length) {
    problems.push(`файлов по ссылкам: ${linksA.length} ≠ ${linksB.length}`);
  }
  for (const link of linksB) {
    const file = join(root, 'public', link.replace(/^\//, ''));
    if (!existsSync(file)) problems.push(`нет файла по ссылке ${link}`);
  }

  const numberA = (ru.frontmatter.match(/^number:\s*(\d+)/m) || [])[1];
  const numberB = (en.frontmatter.match(/^number:\s*(\d+)/m) || [])[1];
  if (numberA !== numberB) problems.push(`number: ${numberA} ≠ ${numberB}`);

  const cyr = cyrillic(en.frontmatter + '\n' + en.body);
  if (cyr > 0) problems.push(`кириллица в переводе: ${cyr} символов`);

  return problems;
}

/** Все пары «русский файл → его en/-двойник» в коллекциях курса. */
export function findPairs() {
  const pairs = [];
  for (const collection of ['topics', 'seminars', 'homework', 'labs', 'results']) {
    const dir = join(contentDir, collection);
    const enDir = join(dir, 'en');
    if (!existsSync(enDir)) continue;
    for (const name of readdirSync(enDir)) {
      if (!name.endsWith('.md')) continue;
      const ruPath = join(dir, name);
      if (existsSync(ruPath) && statSync(ruPath).isFile()) pairs.push([ruPath, join(enDir, name)]);
    }
  }
  return pairs;
}

const main = () => {
  const args = process.argv.slice(2);
  const pairs = args.length
    ? args.map((pair) => pair.split(':').map((p) => join(root, p)))
    : findPairs();

  if (pairs.length === 0) {
    console.log('пар нет — нечего проверять');
    return;
  }

  let failed = 0;
  for (const [ruPath, enPath] of pairs) {
    const problems = checkPair(ruPath, enPath);
    const label = relative(root, enPath).replace('src/content/', '');
    if (problems.length === 0) {
      console.log(`ok   ${label}`);
    } else {
      failed += 1;
      console.log(`FAIL ${label}`);
      for (const problem of problems) console.log(`     · ${problem}`);
    }
  }
  if (failed > 0) process.exitCode = 1;
};

if (process.argv[1] && process.argv[1].endsWith('check-en-translation.mjs')) main();
