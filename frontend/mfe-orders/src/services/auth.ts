const API_BASE_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:8080/api/bff'

function buildUrl(path: string): string {
  return `${API_BASE_URL}${path}`
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json()
    return body?.detail ?? 'Erro inesperado ao chamar a API'
  } catch {
    return 'Erro inesperado ao chamar a API'
  }
}

export { buildUrl, parseError }
