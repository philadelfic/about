import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

/** Лекции курса «Обучение с подкреплением». */
const lectures = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/lectures' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    summary: z.string(),
    date: z.string().optional(),
    slides: z.string().optional(),
  }),
});

/** Лабораторные работы. */
const labs = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/labs' }),
  schema: z.object({
    number: z.number(),
    title: z.string(),
    summary: z.string(),
    when: z.string().optional(),
    deliverable: z.string().optional(),
  }),
});

export const collections = { lectures, labs };
