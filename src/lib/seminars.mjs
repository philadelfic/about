/**
 * Язык занятия и адреса-двойники: русская страница в корне курса, английская — в /en/.
 *
 * Правило простое и проверяется тестом: английская запись лежит в подпапке en/
 * (id вида «en/07-saper-4x4»), русская — в корне коллекции с тем же именем файла.
 * Отдельного поля в frontmatter нет: имя файла и есть пара.
 */

/** Язык записи коллекции seminars: 'en' для файлов из подпапки en/, иначе 'ru'. */
export function seminarLang(id) {
  return id.startsWith('en/') ? 'en' : 'ru';
}

/** Адресный слаг записи: 'en/07-saper-4x4' → '07-saper-4x4'. */
export function seminarSlug(id) {
  return id.replace(/^en\//, '');
}

/** id русской записи по любому id: 'en/07-saper-4x4' → '07-saper-4x4'. */
export function ruSeminarId(id) {
  return seminarSlug(id);
}

/** id английской записи по русскому id: '07-saper-4x4' → 'en/07-saper-4x4'. */
export function enSeminarId(id) {
  return `en/${seminarSlug(id)}`;
}
