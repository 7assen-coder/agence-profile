import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from 'react'
import type { AgencePrivate } from '../types/agence'
import * as api from '../api/client'

type AuthState = {
  token: string | null
  agence: AgencePrivate | null
  loading: boolean
}

type AuthContextValue = AuthState & {
  login: (email: string, password: string) => Promise<void>
  register: (data: {
    nom: string
    email: string
    password: string
    telephone?: string
    ville?: string
    description?: string
  }) => Promise<void>
  logout: () => void
  refreshAgence: () => Promise<void>
  setAgence: (a: AgencePrivate | null) => void
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setTokenState] = useState<string | null>(() =>
    localStorage.getItem('agence_token'),
  )
  const [agence, setAgence] = useState<AgencePrivate | null>(null)
  const [loading, setLoading] = useState(() => !!localStorage.getItem('agence_token'))

  const refreshAgence = useCallback(async () => {
    const t = api.getToken()
    if (!t) {
      setAgence(null)
      return
    }
    try {
      const { agence: a } = await api.getMe()
      setAgence(a)
    } catch {
      api.setToken(null)
      setTokenState(null)
      setAgence(null)
    }
  }, [])

  useEffect(() => {
    if (!token) return
    let cancelled = false
    ;(async () => {
      setLoading(true)
      try {
        const { agence: a } = await api.getMe()
        if (!cancelled) setAgence(a)
      } catch {
        if (!cancelled) {
          api.setToken(null)
          setTokenState(null)
          setAgence(null)
        }
      } finally {
        if (!cancelled) setLoading(false)
      }
    })()
    return () => {
      cancelled = true
    }
  }, [token])

  const login = useCallback(async (email: string, password: string) => {
    const res = await api.login({ email, password })
    api.setToken(res.access_token)
    setTokenState(res.access_token)
    setAgence(res.agence)
    setLoading(false)
  }, [])

  const register = useCallback(
    async (data: {
      nom: string
      email: string
      password: string
      telephone?: string
      ville?: string
      description?: string
    }) => {
      await api.register(data)
      await login(data.email, data.password)
    },
    [login],
  )

  const logout = useCallback(() => {
    api.setToken(null)
    setTokenState(null)
    setAgence(null)
    setLoading(false)
  }, [])

  const value = useMemo(
    () => ({
      token,
      agence,
      loading,
      login,
      register,
      logout,
      refreshAgence,
      setAgence,
    }),
    [token, agence, loading, login, register, logout, refreshAgence],
  )

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}
