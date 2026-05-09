import { type FormEvent, useState } from 'react'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { ApiError } from '../api/client'
import { GlassPanel } from '../components/ui/GlassPanel'
import { Input } from '../components/ui/Input'
import { Button } from '../components/ui/Button'

export function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const location = useLocation()
  const from =
    (location.state as { from?: { pathname: string } } | null)?.from?.pathname ??
    '/compte'

  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [pending, setPending] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setPending(true)
    try {
      await login(email, password)
      navigate(from, { replace: true })
    } catch (err) {
      if (err instanceof ApiError) {
        setError(
          err.body?.error === 'identifiants_invalides'
            ? 'Email ou mot de passe incorrect.'
            : err.message,
        )
      } else setError('Erreur réseau.')
    } finally {
      setPending(false)
    }
  }

  return (
    <div className="w-full px-6 py-14 sm:px-10 sm:py-16 lg:px-14">
    <div className="mx-auto w-full max-w-md">
      <GlassPanel>
        <h1 className="text-2xl font-bold text-slate-900">Connexion</h1>
        <p className="mt-1 text-sm text-slate-600">
          Pas encore de compte ?{' '}
          <Link
            to="/inscription"
            className="cursor-pointer font-semibold text-teal-700 underline decoration-teal-400/70 underline-offset-2 hover:text-teal-900"
          >
            Inscription
          </Link>
        </p>

        <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-4">
          <Input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            label="Mot de passe"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          {error && (
            <p className="rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-800 ring-1 ring-rose-200" role="alert">
              {error}
            </p>
          )}

          <Button type="submit" disabled={pending} className="mt-2 w-full">
            {pending ? 'Connexion…' : 'Se connecter'}
          </Button>
        </form>
      </GlassPanel>
    </div>
    </div>
  )
}
