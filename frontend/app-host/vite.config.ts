import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import federation from '@originjs/vite-plugin-federation'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vueDevTools(),
    federation({
      name: 'shell',
      remotes: {
        orders: {
          external: process.env.VITE_ORDERS_MFE_URL || 'http://localhost:5174/assets/remoteEntry.js',
          externalType: 'url',
        },
      },
      shared: ['vue', 'vue-router'],
    }),
    vue({
      template: {
        compilerOptions: {
          isCustomElement: (tag) => tag.includes('br-'),
        },
      },
    }),

  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    },
  },
  build: {
    rollupOptions: {
      external: ['stream', 'util'],
    },
  },
  ssr: {
    external: ['stream', 'util'],
  },
})
