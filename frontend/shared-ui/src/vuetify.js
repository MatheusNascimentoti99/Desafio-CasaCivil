export const dsgovTheme = {
  defaultTheme: 'dsgov',
  themes: {
    dsgov: {
      dark: false,
      colors: {
        background: '#f8f8f8',
        surface: '#ffffff',
        primary: '#1351b4',
        secondary: '#2670e8',
        success: '#168821',
        warning: '#ffcd07',
        error: '#e52207',
        info: '#2670e8',
      },
    },
  },
}

export const dsgovDefaults = {
  VCard: {
    rounded: 'lg',
    elevation: 0,
    variant: 'flat',
  },
  VBtn: {
    rounded: 'lg',
    style: 'text-transform: none; letter-spacing: 0;',
  },
  VTextField: {
    variant: 'outlined',
    density: 'comfortable',
    hideDetails: 'auto',
  },
  VAlert: {
    rounded: 'lg',
  },
}

export function createDsgovVuetifyOptions(overrides = {}) {
  return {
    theme: dsgovTheme,
    defaults: dsgovDefaults,
    ...overrides,
  }
}
