import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://ernestyalumni-links.vercel.app',
  output: 'static',
  build: {
    inlineStylesheets: 'always',
  },
});
