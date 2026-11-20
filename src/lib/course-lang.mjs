/**
 * Язык записи и адреса-двойники для всех разделов курса.
 *
 * Правило одно и проверяется тестом: английская запись лежит в подпапке en/ той же
 * коллекции (id вида «en/04-iterativnoe-ocenivanie»), русская — в корне с тем же
 * именем файла. Отдельного поля в frontmatter нет: имя файла и есть пара.
 */

/** Язык записи: 'en' для файлов из подпапки en/, иначе 'ru'. */
export function contentLang(id) {
  return id.startsWith('en/') ? 'en' : 'ru';
}

/** Адресный слаг: 'en/04-tema' → '04-tema'. */
export function contentSlug(id) {
  return id.replace(/^en\//, '');
}

/** id английской записи по русскому id. */
export function enContentId(id) {
  return `en/${contentSlug(id)}`;
}

/** Отфильтровать опубликованные записи нужного языка. */
export function published(items, lang) {
  return items.filter((item) => !item.data.draft && contentLang(item.id) === lang);
}
