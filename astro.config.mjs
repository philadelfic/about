import { defineConfig } from 'astro/config';

// Портал живёт на GitHub Pages: https://philadelfic.github.io/about/
export default defineConfig({
  site: 'https://philadelfic.github.io',
  base: '/about',
  trailingSlash: 'ignore',
  build: { format: 'directory' },
});
