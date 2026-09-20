import { defineConfig } from 'astro/config';

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

// Портал живёт на GitHub Pages: https://philadelfic.github.io/about/
export default defineConfig({
  site: 'https://philadelfic.github.io',
  base,
  trailingSlash: 'ignore',
  build: { format: 'directory' },
  markdown: { rehypePlugins: [rehypeBaseImages] },
});
