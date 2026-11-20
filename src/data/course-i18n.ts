/**
 * Тексты «обвязки» курса: то, что печатают страницы вокруг содержимого.
 * Русский и английский рядом, чтобы перевод нельзя было забыть в одном месте.
 *
 * Группы занятия помечены в содержимом как «А» и «Б» — в английской версии это A и B,
 * поэтому подписи собираются функциями, а не строками.
 */
import type { Lang } from './i18n';

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
    courseShort: 'Курс',
    // навигация
    navTopics: 'Темы',
    navHomework: 'Домашние задания',
    navLabs: 'Лабораторные',
    navSeminars: 'Семинарские занятия',
    navResults: 'Результаты',
    navSessions: 'Занятия',
    navTasks: 'Задания',
    navChecks: 'Проверки',
    navTopicsDone: 'Пройденные темы',
    navLabsShort: 'Лабораторные',
    navGroup: 'Группа',
    navVariant: 'Вариант',
    navDue: 'к',
    navLabWord: 'Лабораторная',
    // общее
    openWord: 'Открыть',
    due: 'Срок',
    submitBy: 'Сдать',
    lectureWord: 'лекция',
    lecturesWord: 'лекции',
    // занятие (семинар)
    seminarLabel: 'Семинарское занятие',
    seminarWord: 'Занятие',
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
    materialsTitle: 'Материалы',
    tocTitle: 'Содержание занятия',
    seminarsTitle: 'Семинарские занятия',
    seminarsLead: 'Что разбирали на семинарах и материалы к ним.',
    seminarsEmpty: 'Занятий пока не было — материалы появятся после первого семинара.',
    // тема
    topicWord: 'Тема',
    topicsTitle: 'Темы',
    topicsLead: 'Пройденные темы: что разбирали, теория и вопросы-ответы.',
    topicsEmpty: 'Пока тем нет.',
    coveredOnLecture: (n?: number, date?: string) =>
      n
        ? `Что разбирали на лекции ${n}${date ? ` · ${date}` : ''}`
        : 'Что разбирали на лекции',
    coveredMany: 'Что разбирали',
    lectureGroupTitle: (n: number, date?: string) => `Лекция ${n}${date ? ` · ${date}` : ''}`,
    lecturesHeadline: (numbers: string, many: boolean) =>
      ` · ${many ? 'лекции' : 'лекция'} ${numbers}`,
    qaTitle: 'Вопросы и ответы',
    termsTitle: 'Терминология',
    termCol: 'Термин',
    meaningCol: 'Что это',
    relatedHomework: 'Задания по теме',
    relatedLabs: 'Лабораторные по теме',
    prevTopic: 'Тема',
    topicTocTitle: 'Содержание темы',
    simulatorTitle: 'Покрутить руками',
    // домашние задания
    homeworkWord: 'Домашнее задание',
    homeworkTitle: 'Домашние задания',
    homeworkLead:
      'Баллы за домашние задания идут сверх лабораторных: так можно добрать недостающее до зачёта. Это те же задачи, что разбирали на занятиях, — с продолжением и своими числами.',
    homeworkEmpty: 'Пока заданий нет.',
    homeworkByLecture: (n: number) => ` · лекция ${n}`,
    homeworkBySeminar: (n: number) => ` · семинар ${n}`,
    homeworkByTopic: (n: number) => ` · тема ${n}`,
    // лабораторные
    labWord: 'Лабораторная работа',
    labsTitle: 'Лабораторные работы',
    labsLead:
      'Лабораторные работы курса: обязательные, каждая — с кодом, таблицами и вопросами. Здесь — условие, сроки, файлы и пошаговое руководство по каждой.',
    labsEmpty: 'Пока лабораторных нет.',
    labTocTitle: 'Содержание',
    // результаты
    resultsWord: 'Результаты',
    resultsLead: 'Проверки по занятиям: зачёт или незачёт по заданию и что стоит подтянуть.',
    resultsEmpty: 'Результатов пока нет — появятся после проверки заданий первого занятия.',
    resultsCheck: 'Результаты проверки',
    checkWord: 'Семинар',
    resultsPageTitle: (n: number, title: string) => `Семинар ${n}. ${title} — результаты проверки`,
    resultsH1: (n: number, title: string) => `Семинар ${n}. ${title}`,
    resultsCheckLine: (n: number) => `Результаты проверки · семинар ${n}`,
    resultsColumn: (n: number) => `Семинар ${n}`,
    groupWord: 'Группа',
    sessionWord: 'занятие',
    passWord: 'Зачёт',
    failWord: 'Незачёт',
    totalWord: 'Всего',
    studentCol: 'Студент',
    improveCol: 'Что подтянуть',
    noResults: 'Результатов пока нет.',
    resultsSummary: (group: string, date: string | undefined, passed: number, failed: number, total: number) =>
      `Группа ${group}${date ? ` · занятие ${date}` : ''} · Зачёт: ${passed}${failed > 0 ? ` · Незачёт: ${failed}` : ''} · Всего: ${total}`,
    resultsListLine: (passed: number, total: number, groups: number) =>
      `Зачёт: ${passed} из ${total}.${groups > 1 ? ' Группа — на странице переключателем.' : ''}`,
    resultsGroupPrefix: (names: string[]) =>
      names.length === 1 ? `Группа ${names[0]}. ` : `Группы: ${names.join(' · ')}. `,
    // витрина курса
    landingOverline: 'Т1 + МАИ · магистратура',
    landingTitle: 'Обучение с подкреплением',
    landingLead:
      'Материалы курса: темы, домашние задания, лабораторные работы, семинарские занятия и результаты заданий.',
    landingNote: 'Материалы добавляются по мере прохождения занятий.',
    cardTopics: (count: number) =>
      `Пройденные темы: что разбирали, теория и вопросы-ответы. Сейчас открыто: ${count}.`,
    cardHomework: (count: number) =>
      count > 0
        ? `Домашние задания: баллы сверх лабораторных — можно добрать (заданий: ${count}).`
        : 'Домашние задания: баллы сверх лабораторных — так можно добрать недостающее.',
    cardLabs: (issued: number, all: number) =>
      issued > 0
        ? `Лабораторные работы: обязательные, каждая с кодом и таблицами (выдано ${issued} из ${all}).`
        : 'Лабораторные работы: обязательные, каждая с кодом и таблицами.',
    cardSeminars: (count: number) =>
      count > 0
        ? `Материалы занятий: что разбирали и что можно повторить (занятий: ${count}).`
        : 'Материалы занятий: что разбирали и что можно повторить.',
    cardResults: (count: number) =>
      count > 0 ? `Зачёты по заданиям занятий: ${count}.` : 'Зачёты и незачёты по заданиям занятий.',
    russianOnly: '',
    translationNote: '',
  },
  en: {
    courseTitle: 'T1 + MAI · Reinforcement Learning',
    courseShort: 'Course',
    navTopics: 'Topics',
    navHomework: 'Homework',
    navLabs: 'Labs',
    navSeminars: 'Seminar sessions',
    navResults: 'Results',
    navSessions: 'Sessions',
    navTasks: 'Tasks',
    navChecks: 'Checks',
    navTopicsDone: 'Topics covered',
    navLabsShort: 'Labs',
    navGroup: 'Group',
    navVariant: 'Variant',
    navDue: 'due',
    navLabWord: 'Lab',
    openWord: 'Open',
    due: 'Due',
    submitBy: 'Due',
    lectureWord: 'lecture',
    lecturesWord: 'lectures',
    seminarLabel: 'Seminar session',
    seminarWord: 'Session',
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
    materialsTitle: 'Materials',
    tocTitle: 'Contents of the session',
    seminarsTitle: 'Seminar sessions',
    seminarsLead: 'What we covered in class and the materials for it.',
    seminarsEmpty: 'No sessions yet — materials appear after the first seminar.',
    topicWord: 'Topic',
    topicsTitle: 'Topics',
    topicsLead: 'Topics covered: what we went through, the theory and the questions with answers.',
    topicsEmpty: 'No topics yet.',
    coveredOnLecture: (n?: number, date?: string) =>
      n ? `What we covered in lecture ${n}${date ? ` · ${date}` : ''}` : 'What we covered in the lecture',
    coveredMany: 'What we covered',
    lectureGroupTitle: (n: number, date?: string) => `Lecture ${n}${date ? ` · ${date}` : ''}`,
    lecturesHeadline: (numbers: string, many: boolean) =>
      ` · ${many ? 'lectures' : 'lecture'} ${numbers}`,
    qaTitle: 'Questions and answers',
    termsTitle: 'Terminology',
    termCol: 'Term',
    meaningCol: 'What it means',
    relatedHomework: 'Homework for this topic',
    relatedLabs: 'Labs for this topic',
    prevTopic: 'Topic',
    topicTocTitle: 'Contents of the topic',
    simulatorTitle: 'Try it yourself',
    homeworkWord: 'Homework',
    homeworkTitle: 'Homework',
    homeworkLead:
      'Homework points come on top of the labs: this is how you can make up what is missing for a pass. These are the same tasks we went through in class — continued, with your own numbers.',
    homeworkEmpty: 'No homework yet.',
    homeworkByLecture: (n: number) => ` · lecture ${n}`,
    homeworkBySeminar: (n: number) => ` · seminar ${n}`,
    homeworkByTopic: (n: number) => ` · topic ${n}`,
    labWord: 'Laboratory work',
    labsTitle: 'Laboratory works',
    labsLead:
      'The course labs: all of them are mandatory, each comes with code, tables and questions. Here you find the assignment, deadlines, files and a step-by-step guide for each.',
    labsEmpty: 'No labs yet.',
    labTocTitle: 'Contents',
    resultsWord: 'Results',
    resultsLead: 'Checks by session: pass or fail on the assignment and what is worth revisiting.',
    resultsEmpty: 'No results yet — they appear after the first session is checked.',
    resultsCheck: 'Check results',
    checkWord: 'Session',
    resultsPageTitle: (n: number, title: string) => `Session ${n}. ${title} — check results`,
    resultsH1: (n: number, title: string) => `Session ${n}. ${title}`,
    resultsCheckLine: (n: number) => `Check results · session ${n}`,
    resultsColumn: (n: number) => `Session ${n}`,
    groupWord: 'Group',
    sessionWord: 'session',
    passWord: 'Pass',
    failWord: 'Fail',
    totalWord: 'Total',
    studentCol: 'Student',
    improveCol: 'What to revisit',
    noResults: 'No results yet.',
    resultsSummary: (group: string, date: string | undefined, passed: number, failed: number, total: number) =>
      `Group ${group}${date ? ` · session ${date}` : ''} · Pass: ${passed}${failed > 0 ? ` · Fail: ${failed}` : ''} · Total: ${total}`,
    resultsListLine: (passed: number, total: number, groups: number) =>
      `Pass: ${passed} of ${total}.${groups > 1 ? ' The group is switched on the page.' : ''}`,
    resultsGroupPrefix: (names: string[]) =>
      names.length === 1 ? `Group ${names[0]}. ` : `Groups: ${names.join(' · ')}. `,
    landingOverline: 'T1 + MAI · master’s programme',
    landingTitle: 'Reinforcement Learning',
    landingLead:
      'Course materials: topics, homework, laboratory works, seminar sessions and the results of the assignments.',
    landingNote: 'Materials are added as the course goes on.',
    cardTopics: (count: number) =>
      `Topics covered: what we went through, the theory and the questions with answers. Open now: ${count}.`,
    cardHomework: (count: number) =>
      count > 0
        ? `Homework: points on top of the labs, so you can make up what is missing (tasks: ${count}).`
        : 'Homework: points on top of the labs, so you can make up what is missing.',
    cardLabs: (issued: number, all: number) =>
      issued > 0
        ? `Laboratory works: all mandatory, each with code and tables (issued ${issued} of ${all}).`
        : 'Laboratory works: all mandatory, each with code and tables.',
    cardSeminars: (count: number) =>
      count > 0
        ? `Materials of the sessions: what we covered and what can be repeated (sessions: ${count}).`
        : 'Materials of the sessions: what we covered and what can be repeated.',
    cardResults: (count: number) =>
      count > 0 ? `Checks of the session assignments: ${count}.` : 'Passes and fails on the session assignments.',
    russianOnly: '',
    translationNote: '',
  },
} as const;

/** Подписи карточек и списков для нужного языка. */
export const chrome = (lang: Lang) => courseChrome[lang];
