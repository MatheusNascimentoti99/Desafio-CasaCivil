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
        './OrdersApp': './src/pages/OrdersApp.vue',
      },
      shared: ['vue'],
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
