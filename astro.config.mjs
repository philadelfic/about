import { defineConfig } from 'astro/config';
import { createIdNamer } from './src/lib/headings.mjs';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

const base = '/about';

/**
 * Картинки в markdown пишем от корня сайта: ![подпись](/img/course/rl/step.png).
 * Этот плагин добавляет к таким путям базовый префикс → /about/img/course/rl/step.png.
 */
function rehypeBaseImages() {
  return (tree) => {
    const walk = (node) => {
      if (
        node.type === 'element' &&
        node.tagName === 'img' &&
        typeof node.properties?.src === 'string' &&
        node.properties.src.startsWith('/')
      ) {
        node.properties.src = base + node.properties.src;
      }
      if (Array.isArray(node.children)) node.children.forEach(walk);
    };
    walk(tree);
  };
}

function collectText(node) {
  if (node.type === 'text') return node.value;
  if (Array.isArray(node.children)) return node.children.map(collectText).join('');
  return '';
}

/**
 * Расставляем id заголовкам теории — по ним скачет оглавление в левом меню.
 * Алгоритм тот же, что в src/lib/headings.mjs (общий с содержанием темы и якорями вопросов),
 * поэтому ссылки в оглавлении совпадают.
 */
function rehypeHeadingIds() {
  return (tree) => {
    const namer = createIdNamer();
    const walk = (node) => {
      if (node.type === 'element' && /^h[23]$/.test(node.tagName)) {
        const id = namer.claim(collectText(node));
        node.properties = { ...(node.properties || {}), id };
      }
      if (Array.isArray(node.children)) node.children.forEach(walk);
    };
    walk(tree);
  };
}

// Портал живёт на GitHub Pages: https://philadelfic.github.io/about/
export default defineConfig({
  site: 'https://philadelfic.github.io',
  base,
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  markdown: {
    remarkPlugins: [remarkMath],
    rehypePlugins: [rehypeBaseImages, rehypeKatex, rehypeHeadingIds],
  },
});
