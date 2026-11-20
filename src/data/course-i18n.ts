/**
 * Тексты «обвязки» курса: то, что печатает страница занятия вокруг содержимого.
 * Русский и английский рядом, чтобы перевод нельзя было забыть в одном месте.
 *
 * Группы занятия помечены в содержимом как «А» и «Б» — в английской версии это A и B,
 * поэтому подписи собираются функциями, а не строками.
 */
import type { Lang } from './i18n';

export type Group = 'А' | 'Б';

const groupEn: Record<string, string> = { 'А': 'A', 'Б': 'B' };

/** Подпись группы для зала: «Группа А» / «Group A». */
export function groupLabel(group: string, lang: Lang): string {
  return lang === 'en' ? `Group ${groupEn[group] ?? group}` : `Группа ${group}`;
}

/** Подпись варианта рубежного контроля. */
export function variantLabel(group: string, lang: Lang): string {
  return lang === 'en' ? `Variant ${groupEn[group] ?? group}` : `Вариант ${group}`;
}

/** Подпись ссылки-якоря ответа: в скринридере список ссылок должен читаться осмысленно. */
export function answerAnchorLabel(title: string, lang: Lang): string {
  const line = title.replace(/\s+/g, ' ').trim();
  const short = line.length > 60 ? `${line.slice(0, 60)}…` : line;
  return lang === 'en' ? `Link to the question: ${short}` : `Ссылка на вопрос: ${short}`;
}

export const courseChrome = {
  ru: {
    courseTitle: 'Т1 + МАИ · Обучение с подкреплением',
    seminarLabel: 'Семинарское занятие',
    coveredTitle: 'Что было на занятии',
    theoryTitle: 'Теория',
    tasksTitle: 'Задачи для проверки понимания материала',
    tasksEmpty: (group: string) => `Задачи для группы ${group} появятся позже.`,
    answer: 'Ответ',
    quizTitle: (number: number) => `Рубежный контроль №${number}`,
    quizLead:
      'Двенадцать вопросов, 12 баллов, 12 минут: десять с выбором ответа и два — своими словами. Вариант — по вашей группе. Ответы спрятаны: сначала отвечаете сами, потом сверяетесь.',
    groupAria: 'Группа занятия',
    variantAria: 'Вариант рубежного контроля',
    due: 'Срок',
    materialsTitle: 'Материалы',
    tocTitle: 'Содержание занятия',
    seminarWord: 'Занятие',
    seminarsTitle: 'Семинарские занятия',
    seminarsLead: 'Что разбирали на семинарах и материалы к ним.',
    seminarsEmpty: 'Занятий пока не было — материалы появятся после первого семинара.',
    russianOnly: '',
    translationNote: '',
  },
  en: {
    courseTitle: 'T1 + MAI · Reinforcement Learning',
    seminarLabel: 'Seminar session',
    coveredTitle: 'What happened in class',
    theoryTitle: 'Theory',
    tasksTitle: 'Questions to check your understanding',
    tasksEmpty: (group: string) => `Questions for group ${group} will appear later.`,
    answer: 'Answer',
    quizTitle: (number: number) => `Progress test #${number}`,
    quizLead:
      'Twelve questions, 12 points, 12 minutes: ten multiple-choice and two in your own words. The variant depends on your group. Answers are hidden: answer first, then check.',
    groupAria: 'Group of the session',
    variantAria: 'Progress test variant',
    due: 'Due',
    materialsTitle: 'Materials',
    tocTitle: 'Contents of the session',
    seminarWord: 'Session',
    seminarsTitle: 'Seminar sessions',
    seminarsLead: 'What we covered in class and the materials for it.',
    seminarsEmpty: 'No sessions yet — materials appear after the first seminar.',
    russianOnly: 'Слайды презентации — на русском',
    translationNote: '',
  },
} as const;
