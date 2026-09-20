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
    materials: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
    /** Заготовка формата — не показывается на сайте. */
    draft: z.boolean().default(false),
  }),
});

export const collections = { topics, homework, seminars };
