const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8080/api/bff'

function buildUrl(path: string): string {
  return `${API_BASE_URL}${path}`
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json()
    const detail = body?.detail

    if (typeof detail === 'string' && detail) {
      return detail
    }

    if (Array.isArray(detail) && detail.length > 0) {
      return detail
        .map((entry) => {
          if (typeof entry?.msg !== 'string') {
            return ''
          }

          const loc = Array.isArray(entry?.loc) ? entry.loc : []
          const field = loc.length > 0 ? String(loc[loc.length - 1]) : ''
          return field ? `${field}: ${entry.msg}` : entry.msg
        })
        .filter(Boolean)
        .join(' | ')
    }

    return 'Erro inesperado ao chamar a API'
  } catch {
    return 'Erro inesperado ao chamar a API'
  }
}

export { buildUrl, parseError }
