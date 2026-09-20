import { getCollection, type CollectionEntry } from 'astro:content';

/**
 * Коллекция может быть пустой (например, «семинары» до первого занятия) — Astro в этом случае
 * бросает ошибку. Считаем такую коллекцию просто пустым списком.
 */
export async function optionalCollection<K extends 'topics' | 'homework' | 'seminars'>(
  name: K
): Promise<CollectionEntry<K>[]> {
  try {
    return await getCollection(name);
  } catch {
    return [];
  }
}
