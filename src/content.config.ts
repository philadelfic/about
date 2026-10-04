import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** Темы курса: теория и вопросы-ответы. Добавляем по мере прохождения. */
const topics = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/topics' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    summary: z.string(),
    date: z.string().optional(),
    /** Что разбирали на лекции — короткие тезисы-ориентиры. */
    covered: z.array(z.string()).default([]),
    /** Лекции, которые закрывает тема: номер, дата и что разбирали. */
    lectures: z
      .array(
        z.object({
          number: z.number(),
          date: z.string().optional(),
          covered: z.array(z.string()).default([]),
        })
      )
      .default([]),
    /** Вопросы и ответы по теме. */
    qa: z.array(z.object({ q: z.string(), a: z.string() })).default([]),
    /** Терминология темы — списком в конце. */
    terms: z.array(z.object({ term: z.string(), definition: z.string() })).default([]),
    /** Ссылки на материалы темы (слайды, конспекты) — появляются, когда есть. */
    lecture: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
    /**
     * Пресет мини-симулятора: 'l2' — две панели (детерминированный лабиринт и холодильник),
     * 'l3' — одна панель лабиринта со сносами 0,8 / 0,1 / 0,1. Поле отсутствует — панелей нет.
     */
    simulator: z.enum(['l2', 'l3']).optional(),
  }),
});

/** Домашние задания. */
const homework = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/homework' }),
  schema: z.object({
    title: z.string(),
    summary: z.string().default(''),
    due: z.string().optional(),
    topic: z.number().optional(),
    /** Номер лекции, к которой относится задание (может отличаться от номера темы). */
    lecture: z.number().optional(),
  }),
});

/** Семинарские занятия. */
const seminars = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/seminars' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    summary: z.string(),
    date: z.string().optional(),
    /** Что разбирали на занятии — короткие тезисы-ориентиры. */
    covered: z.array(z.string()).default([]),
    /** Задачи для проверки понимания; group — группа занятия (А / Б), пусто — задача общая для обеих групп; ответ показываем, когда он есть. */
    tasks: z
      .array(
        z.object({
          group: z.string().default(''),
          title: z.string(),
          text: z.string(),
          answer: z.string().optional(),
        })
      )
      .default([]),
    /** Рубежный контроль: вопросы по вариантам занятия; группа А / Б, пусто — вопрос общий. */
    quiz: z
      .array(
        z.object({
          group: z.string().default(''),
          title: z.string(),
          text: z.string(),
          options: z.array(z.string()).default([]),
          answer: z.string().optional(),
        })
      )
      .default([]),
    materials: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
    /** Заготовка формата — не показывается на сайте. */
    draft: z.boolean().default(false),
  }),
});

/** Одна строка результатов: студент, зачёт/незачёт и темы, которые стоит повторить. */
const resultRow = z.object({
  student: z.string(),
  status: z.enum(['зачёт', 'незачёт']),
  /** Разделы портала, где это разобрано подробнее (путь без base, можно с якорем). */
  links: z.array(z.object({ title: z.string(), href: z.string() })).default([]),
});

/** Результаты заданий занятий: проверка одна на занятие, группы — на странице переключателем. */
const results = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/results' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    summary: z.string().default(''),
    /** Группы, у которых прошла проверка; порядок — как в файле (сначала гр.1). */
    groups: z
      .array(
        z.object({
          /** Название группы, как в расписании; оно же на кнопке переключателя. */
          name: z.string(),
          /** Дата занятия этой группы. */
          date: z.string().optional(),
          /** Строки читают по алфавиту, а не по баллам. */
          rows: z.array(resultRow).default([]),
        })
      )
      .default([]),
    /** Заготовка формата — не показывается на сайте. */
    draft: z.boolean().default(false),
  }),
});

export const collections = { topics, homework, seminars, results };
