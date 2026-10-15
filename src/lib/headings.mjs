/**
 * Единое место, где рождаются id заголовков и якорей: rehype-плагин в astro.config.mjs,
 * содержание темы/занятия и якоря вопросов-ответов. Алгоритм один: slugify от текста,
 * первый повтор получает суффикс -1, второй -2 и так далее — поэтому ссылки в оглавлении,
 * в контенте (например, из «Результатов») и в разметке всегда совпадают.
 */
import { slugify } from './slug.mjs';

/**
 * Раздаёт уникальные id по текстам: первое «введение» → введение, второе → введение-1.
 * Каждый вызов `claim` учитывается в общем счётчике, поэтому заголовки теории и якоря
 * вопросов внутри одной страницы не сталкиваются — так было и раньше, см. темы/семинары.
 * fallback подставляется, когда из текста не осталось слова (например, заголовок из смайлов).
 */
export function createIdNamer() {
  const used = new Map();
  return {
    claim(text, fallback = 'section') {
      const base = slugify(text) || fallback;
      const count = used.get(base) ?? 0;
      used.set(base, count + 1);
      return count > 0 ? `${base}-${count}` : base;
    },
  };
}

/**
 * Заголовки ## и ### из тела markdown в порядке следования: текст без **, готовый id
 * и уровень (1 — ##, 2 — ###). Остальные уровни не берём: они в оглавление не попадали.
 * namer передаётся снаружи, когда якоря страницы продолжают нумерацию заголовков (темы);
 * без него создаётся свой.
 */
export function bodyHeadings(body, namer = createIdNamer()) {
  const headings = [];
  for (const raw of (body ?? '').split('\n')) {
    const match = /^(##|###)\s+(.*)$/.exec(raw.trim());
    if (!match) continue;
    const text = match[2].replace(/\*\*/g, '').trim();
    headings.push({ text, id: namer.claim(text), level: match[1] === '###' ? 2 : 1 });
  }
  return headings;
}
