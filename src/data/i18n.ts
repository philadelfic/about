export type Lang = 'ru' | 'en';

export const dict = {
  ru: {
    siteName: 'Олег Орловский',
    title: 'Олег Орловский — проекты и материалы студентам',
    description:
      'Личный портал: ИТ-лид команды разработки, преподаю обучение с подкреплением, делаю инструменты для работы с LLM-харнесами.',
    nav: { projects: 'Проекты', students: 'Студентам', me: 'Обо мне' },
    theme: { toDark: 'Тёмная тема', toLight: 'Светлая тема' },
    langLabel: 'Язык',
    skipToContent: 'К основному содержанию',
  },
  en: {
    siteName: 'Oleg Orlovsky',
    title: 'Oleg Orlovsky — projects and study materials',
    description:
      'Personal site: IT lead of a development team, teaching reinforcement learning, building tools for LLM harnesses.',
    nav: { projects: 'Projects', students: 'Students', me: 'About' },
    theme: { toDark: 'Dark theme', toLight: 'Light theme' },
    langLabel: 'Language',
    skipToContent: 'Skip to content',
  },
} as const;
