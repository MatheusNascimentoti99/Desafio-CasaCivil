import { fileURLToPath, URL } from 'node:url'

import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'
import federation from '@originjs/vite-plugin-federation'

// https://vite.dev/config/
export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const ordersRemoteUrl =
    env.VITE_ORDERS_MFE_URL ||
    process.env.VITE_ORDERS_MFE_URL ||
    'http://localhost:3001/assets/remoteEntry.js'
  const catalogRemoteUrl =
    env.VITE_CATALOG_MFE_URL ||
    process.env.VITE_CATALOG_MFE_URL ||
    'http://localhost:3002/assets/remoteEntry.js'

  return {
  plugins: [
    vueDevTools(),
    federation({
      name: 'shell',
      remotes: {
        orders: {
          external: ordersRemoteUrl,
          externalType: 'url',
        },
        catalog: {
          external: catalogRemoteUrl,
          externalType: 'url',
        },
      },
      shared: ['vue', 'vue-router', 'vuetify'],
    }),
    vue(),

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
}
})
