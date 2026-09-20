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
  title: 'Олег Орловский — проекты, статьи, материалы студентам',
  description:
    'Личный портал: что я делаю, как идут проекты, статьи и учебные материалы по обучению с подкреплением.',
};

export const externalLinks = [
  { title: 'GitHub', href: 'https://github.com/philadelfic', note: 'код и релизы проектов' },
  {
    title: 'Телеграм-канал «Хобби одного атишника»',
    href: 'https://t.me/HobbyOdnogoITishnika',
    note: 'заметки о GitHub, столярке, технике, мыслях',
  },
];
