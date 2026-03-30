import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import federation from '@originjs/vite-plugin-federation'

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: 'catalog',
      filename: 'remoteEntry.js',
      exposes: {
        './CatalogCrud': './src/pages/CatalogCrudPage.vue',
      },
      shared: ['vue', 'vuetify', 'vue-router'],
    }),
  ],
  build: {
    target: 'esnext',
    minify: false,
    rollupOptions: {
      external: ['stream', 'util'],
    },
  },
  ssr: {
    external: ['stream', 'util'],
  },
})
