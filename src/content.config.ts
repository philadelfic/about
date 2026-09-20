import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** Темы курса: теория, вопросы-ответы и материалы прошедших занятий. */
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
    /** Файлы и ссылки по лекции (слайды, конспекты). */
    lecture: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
    /** Файлы и ссылки по семинару. */
    seminar: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
  }),
});

/** Домашние задания. */
const homework = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/homework' }),
  schema: z.object({
    title: z.string(),
    due: z.string().optional(),
    topic: z.number().optional(),
  }),
});

export const collections = { topics, homework };
