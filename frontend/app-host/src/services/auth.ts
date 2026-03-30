import type {
  LoginPayload,
  RegisterPayload,
  UserResponse,
} from '@/types/auth'

const API_BASE = import.meta.env.VITE_API_URL ?? 'http://localhost:8080/api/bff'

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
  const response = await fetch(buildUrl('/auth/register'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<UserResponse>
}

export async function loginUser(payload: LoginPayload): Promise<void> {
  const response = await fetch(buildUrl('/auth/login'), {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    credentials: 'include',
    body: JSON.stringify(payload),
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }
}

export async function logoutUser(): Promise<void> {
  await fetch(buildUrl('/auth/logout'), {
    method: 'POST',
    credentials: 'include',
  })
}

export async function getSession(): Promise<UserResponse> {
  const response = await fetch(buildUrl('/session'), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  const body = (await response.json()) as { authenticated: boolean; user: UserResponse }
  return body.user
}

export async function listUsers(): Promise<UserResponse[]> {
  const response = await fetch(buildUrl('/users'), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<UserResponse[]>
}

export async function getCurrentUser(): Promise<UserResponse> {
  const response = await fetch(buildUrl('/users/me'), {
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(await parseError(response))
  }

  return response.json() as Promise<UserResponse>
}
