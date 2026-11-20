/**
 * Занятия: язык и адреса-двойники. Тонкая обёртка над общим правилом курса,
 * чтобы старые импорты (страницы занятий, тесты) остались как были.
 */
import { contentLang, contentSlug, enContentId } from './course-lang.mjs';

/** Язык записи коллекции seminars: 'en' для файлов из подпапки en/. */
export const seminarLang = contentLang;

/** Адресный слаг записи: 'en/07-saper-4x4' → '07-saper-4x4'. */
export const seminarSlug = contentSlug;

/** id русской записи по любому id. */
export const ruSeminarId = contentSlug;

/** id английской записи по русскому id. */
export const enSeminarId = enContentId;
