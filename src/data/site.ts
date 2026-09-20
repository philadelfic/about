/**
 * Общие данные портала: кто я, куда ведут внешние ссылки.
 * Список проектов здесь не дублируется — он живёт в src/content/projects/.
 */

/** BASE_URL в Astro приходит без завершающего слэша — приводим к виду "/about/". */
const rawBase = import.meta.env.BASE_URL || '/';
export const base = rawBase.endsWith('/') ? rawBase : `${rawBase}/`;

/** Склеивает базовый путь с относительным: withBase('projects/') → '/about/projects/'. */
export const withBase = (path = '') => `${base}${path.replace(/^\//, '')}`;

export const site = {
  name: 'Олег Орловский',
  title: 'Олег Орловский — проекты и материалы студентам',
  description:
    'Личный портал: ИТ-лид команды разработки, преподаю обучение с подкреплением, делаю инструменты для работы с LLM.',
};

export const externalLinks = [
  { title: 'GitHub', href: 'https://github.com/philadelfic', note: 'код и релизы проектов' },
  {
    title: 'Телеграм-канал «Хобби одного атишника»',
    href: 'https://t.me/HobbyOdnogoITishnika',
    note: 'личный блог',
  },
];
