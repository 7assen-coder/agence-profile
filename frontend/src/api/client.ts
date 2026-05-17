import type { AgencePrivate, AgencePublic, ApiErrorBody } from '../types/agence'

const BASE = import.meta.env.VITE_API_URL ?? ''

async function parseJson(res: Response): Promise<unknown> {
  const text = await res.text()
  if (!text) return null
  try {
    return JSON.parse(text)
  } catch {
    return { error: 'invalid_json' }
  }
}

export class ApiError extends Error {
  status: number
  body: ApiErrorBody | null

  constructor(status: number, message: string, body: ApiErrorBody | null) {
    super(message)
    this.status = status
    this.body = body
  }
}

export function getToken(): string | null {
  return localStorage.getItem('agence_token')
}

export function setToken(token: string | null) {
  if (token) localStorage.setItem('agence_token', token)
  else localStorage.removeItem('agence_token')
}

async function request<T>(
  path: string,
  options: RequestInit & { token?: string | null } = {},
): Promise<T> {
  const { token = getToken(), ...init } = options
  const headers = new Headers(init.headers)
  if (!(init.body instanceof FormData)) {
    headers.set('Content-Type', 'application/json')
  }
  if (token) headers.set('Authorization', `Bearer ${token}`)

  const res = await fetch(`${BASE}${path}`, { ...init, headers })
  const data = (await parseJson(res)) as T & ApiErrorBody

  if (!res.ok) {
    const err = data as ApiErrorBody
    throw new ApiError(
      res.status,
      err?.error ?? `http_${res.status}`,
      err?.error ? err : null,
    )
  }
  return data as T
}

export function logoUrl(filename: string | null | undefined): string | null {
  if (!filename) return null
  return `${BASE}/api/agences/logos/${encodeURIComponent(filename)}`
}

export async function health(): Promise<{ status: string; module: string }> {
  return request('/api/health')
}

export async function register(payload: {
  nom: string
  email: string
  password: string
  telephone?: string
  ville?: string
  description?: string
  adresse?: string
}): Promise<{ message: string; agence: AgencePrivate }> {
  return request('/api/auth/register', {
    method: 'POST',
    body: JSON.stringify(payload),
    token: null,
  })
}

export async function login(payload: {
  email: string
  password: string
}): Promise<{
  access_token: string
  token_type: string
  agence: AgencePrivate
}> {
  return request('/api/auth/login', {
    method: 'POST',
    body: JSON.stringify(payload),
    token: null,
  })
}

export async function getMe(): Promise<{ agence: AgencePrivate }> {
  return request('/api/agences/me')
}

export async function updateMe(
  payload: Partial<{
    nom: string
    telephone: string
    adresse: string
    ville: string
    description: string
  }>,
): Promise<{ message: string; agence: AgencePrivate }> {
  return request('/api/agences/me', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function uploadLogo(file: File): Promise<{
  message: string
  logo: string
}> {
  const fd = new FormData()
  fd.append('logo', file)
  return request('/api/agences/me/logo', {
    method: 'POST',
    body: fd,
  })
}

export async function changePassword(payload: {
  ancien_password: string
  nouveau_password: string
}): Promise<{ message: string }> {
  return request('/api/agences/me/password', {
    method: 'PUT',
    body: JSON.stringify(payload),
  })
}

export async function listAgences(params?: {
  page?: number
  per_page?: number
  ville?: string
}): Promise<{
  items: AgencePublic[]
  total: number
  page: number
  pages: number
}> {
  const q = new URLSearchParams()
  if (params?.page) q.set('page', String(params.page))
  if (params?.per_page) q.set('per_page', String(params.per_page))
  if (params?.ville) q.set('ville', params.ville)
  const qs = q.toString()
  return request(`/api/agences${qs ? `?${qs}` : ''}`)
}

export async function getAgencePublic(
  id: number,
): Promise<{ agence: AgencePublic }> {
  return request(`/api/agences/${id}`)
}
