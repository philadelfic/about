/**
 * Продукты и релизы: единственное место, где данные контента превращаются в то, что рисуют страницы.
 * Русский текст лежит в полях без суффикса, английский — в полях *En; релизы разведены полем lang.
 */
import { getCollection } from 'astro:content';

/** Сравнение версий «3.2.0» < «3.10.0»: по числам, а не по строке. */
function versionValue(version) {
  return version
    .split('.')
    .map((part) => Number.parseInt(part, 10) || 0)
    .reduce((acc, part) => acc * 1000 + part, 0);
}

/** Локализованные поля одного продукта. */
export function localizeProject(data, lang = 'ru') {
  const en = lang === 'en';
  return {
    title: data.title,
    slug: data.slug,
    kind: data.kind,
    repo: data.repo,
    stack: en ? data.stackEn ?? data.stack : data.stack,
    order: data.order,
    idea: en ? data.ideaEn : data.idea,
    why: en ? data.whyEn : data.why,
    how: en ? data.howEn : data.how,
    roadmap: data.roadmap.map((item) => (en ? item.textEn : item.text)),
    sections: data.sections.map((section) => ({
      title: en ? section.titleEn : section.title,
      items: section.items.map((item) => (en ? item.textEn : item.text)),
    })),
    links: data.links.map((link) => ({ title: en ? link.titleEn ?? link.title : link.title, href: link.href })),
  };
}

/** Все продукты витрины, по порядку. */
export async function projectsList(lang = 'ru') {
  const all = await getCollection('projects');
  return all
    .filter((entry) => !entry.data.draft)
    .map((entry) => localizeProject(entry.data, lang))
    .sort((a, b) => a.order - b.order);
}

/** Продукт по слагу — для страницы продукта. */
export async function projectBySlug(slug, lang = 'ru') {
  const all = await projectsList(lang);
  return all.find((item) => item.slug === slug);
}

/** Релизы одного продукта на одном языке: от свежих к старым. */
export async function releasesOf(projectSlug, lang = 'ru') {
  const all = await getCollection('releases');
  return all
    .filter(
      (entry) =>
        entry.data.project === projectSlug && entry.data.lang === lang && !entry.data.draft
    )
    .sort((a, b) => versionValue(b.data.version) - versionValue(a.data.version));
}

/**
 * Дата релиза для показа: русская строка («13.10.2026») остаётся как есть,
 * ISO-дата английской версии печатается по-английски («October 13, 2026»).
 */
export function formatReleaseDate(value, lang = 'ru') {
  if (lang !== 'en' || !/^\d{4}-\d{2}-\d{2}$/.test(value)) return value;
  const [year, month, day] = value.split('-').map(Number);
  return new Intl.DateTimeFormat('en-US', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(new Date(Date.UTC(year, month - 1, day)));
}

/** Свежий релиз продукта (или ничего, если версий ещё нет). */
export async function latestRelease(projectSlug, lang = 'ru') {
  return (await releasesOf(projectSlug, lang))[0];
}

/** У релиза есть свой текст — значит, есть и своя страница; иначе ведём на GitHub. */
export function hasBody(entry) {
  return Boolean(entry.body && entry.body.trim().length > 0);
}
