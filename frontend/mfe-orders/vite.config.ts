import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import federation from '@originjs/vite-plugin-federation'

export default defineConfig({
  plugins: [
    vue(),
    federation({
      name: 'orders',
      filename: 'remoteEntry.js',
      exposes: {
        './OrdersList': './src/pages/OrdersListPage.vue',
        './OrderCreate': './src/pages/OrderCreatePage.vue',
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
