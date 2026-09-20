/**
 * Общие данные портала: кто я, куда ведут внешние ссылки.
 * Список проектов здесь не дублируется — он живёт в src/content/projects/.
 */
export const site = {
  name: 'Олег Орловский',
  title: 'Олег Орловский — проекты, статьи, материалы студентам',
  description:
    'Личный портал: что я делаю, как идут проекты, статьи и учебные материалы по обучению с подкреплением.',
  base: import.meta.env.BASE_URL,
};

export const externalLinks = [
  { title: 'Резюме', href: 'https://philadelfic.github.io/resume/', note: 'опыт, навыки, проекты' },
  { title: 'GitHub', href: 'https://github.com/philadelfic', note: 'код и релизы проектов' },
  { title: 'Телеграм-канал «Хобби одного атишника»', href: 'https://t.me/HobbyOdnogoITishnika', note: 'заметки о GitHub, столярке, технике, мыслях' },
];
