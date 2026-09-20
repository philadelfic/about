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
    'Личный портал: ИТ-лид команды разработки, преподаю обучение с подкреплением, делаю инструменты для работы с LLM-харнесами.',
};

export const links = {
  github: 'https://github.com/philadelfic',
  telegram: 'https://t.me/HobbyOdnogoITishnika',
  /** Чат группы курса «Обучение с подкреплением» (Т1 + МАИ). */
  chat: 'https://t.me/+7J1lFtldA3o3YWIy',
};

export const externalLinks = [
  { title: 'GitHub', href: links.github, note: 'код и релизы проектов' },
  {
    title: 'Телеграм-канал «Хобби одного айтишника»',
    href: links.telegram,
    note: 'личный блог',
  },
];

/**
 * Код доступа к материалам курса (мягкая защита: это статика, содержимое страниц лежит в HTML).
 * scope — пути от корня сайта, которые закрыты кодом; hash — FNV-1a(код в нижнем регистре) в hex.
 * Сам код в репозитории не храним (репозиторий публичный).
 * Сменить код: node scripts/gate-hash.mjs <новый код> и подставить хэш сюда.
 */
export const gate = {
  scope: ['students/mai'],
  hash: 'a038a15f', // код согласован с Олегом 20.09.2026; при вводе регистр не важен
  key: 'about.gate',
};
