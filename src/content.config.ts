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
    /** Задачи для проверки понимания; group — группа занятия (А / Б), ответ показываем, когда он есть. */
    tasks: z
      .array(
        z.object({
          group: z.string().default('А'),
          title: z.string(),
          text: z.string(),
          answer: z.string().optional(),
        })
      )
      .default([]),
    materials: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
    /** Заготовка формата — не показывается на сайте. */
    draft: z.boolean().default(false),
  }),
});

/** Результаты заданий занятий: зачёт или незачёт по каждому студенту группы. */
const results = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/results' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    date: z.string().optional(),
    /** Группа, у которой прошёл семинар, — как в расписании. */
    group: z.string().optional(),
    summary: z.string().default(''),
    /** Студент, результат по заданию семинара и темы, которые стоит повторить; порядок на странице — по алфавиту. */
    rows: z
      .array(
        z.object({
          student: z.string(),
          status: z.enum(['зачёт', 'незачёт']),
          /** Разделы портала, где это разобрано подробнее (путь без base, можно с якорем). */
          links: z.array(z.object({ title: z.string(), href: z.string() })).default([]),
        })
      )
      .default([]),
    /** Заготовка формата — не показывается на сайте. */
    draft: z.boolean().default(false),
  }),
});

export const collections = { topics, homework, seminars, results };
