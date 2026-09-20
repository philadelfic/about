/** Одна и та же функция для заголовков теории: и в rehype-плагине, и в оглавлении темы. */
export function slugify(text) {
  return String(text)
    .toLowerCase()
    .replace(/[^\p{L}\p{N}\s-]/gu, '')
    .trim()
    .replace(/\s+/g, '-');
}
