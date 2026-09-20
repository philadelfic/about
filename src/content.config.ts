import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** Темы курса: материалы прошедших лекций и семинаров. Добавляем по мере прохождения. */
const topics = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/topics' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    summary: z.string(),
    date: z.string().optional(),
    lecture: z.array(z.object({ title: z.string(), href: z.string().optional() })).default([]),
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
