import type {
  LoginPayload,
  RegisterPayload,
  TokenResponse,
  UserResponse,
} from '@/types/auth'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8080'

function buildUrl(path: string): string {
  return `${API_BASE}${path}`
}

async function parseError(response: Response): Promise<string> {
  try {
    const body = await response.json()
    return body?.detail ?? 'Erro inesperado'
  } catch {
    return 'Erro inesperado'
  }
}

export async function registerUser(payload: RegisterPayload): Promise<UserResponse> {
  const response = await fetch(buildUrl('/api/auth/register'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<UserResponse>
}

export async function loginUser(payload: LoginPayload): Promise<TokenResponse> {
  const response = await fetch(buildUrl('/api/auth/login'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<TokenResponse>
}

export async function getCurrentUser(token: string): Promise<UserResponse> {
  const response = await fetch(buildUrl('/api/auth/users/me'), {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<UserResponse>
}
