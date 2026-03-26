interface ImportMetaEnv {
  readonly VITE_API_URL?: string
  readonly VITE_ORDERS_MFE_URL?: string
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}

declare module 'vuetify/styles'
