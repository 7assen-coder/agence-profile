import { type FormEvent, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { ApiError } from '../api/client'
import { GlassPanel } from '../components/ui/GlassPanel'
import { Input, TextArea } from '../components/ui/Input'
import { Button } from '../components/ui/Button'

export function RegisterPage() {
  const { register } = useAuth()
  const navigate = useNavigate()

  const [nom, setNom] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [telephone, setTelephone] = useState('')
  const [ville, setVille] = useState('')
  const [description, setDescription] = useState('')
  const [error, setError] = useState<string | null>(null)
  const [pending, setPending] = useState(false)

  async function onSubmit(e: FormEvent) {
    e.preventDefault()
    setError(null)
    setPending(true)
    try {
      await register({
        nom,
        email,
        password,
        telephone: telephone || undefined,
        ville: ville || undefined,
        description: description || undefined,
      })
      navigate('/compte', { replace: true })
    } catch (err) {
      if (err instanceof ApiError) {
        if (err.body?.error === 'email_already_used') {
          setError('Cette adresse e-mail est déjà utilisée.')
        } else if (err.body?.error === 'validation_error' && err.body.details) {
          setError(
            Object.entries(err.body.details)
              .map(([k, v]) => `${k}: ${v.join(', ')}`)
              .join(' · '),
          )
        } else setError(err.message)
      } else setError('Erreur réseau.')
    } finally {
      setPending(false)
    }
  }

  return (
    <div className="w-full px-6 py-14 sm:px-10 sm:py-16 lg:px-14">
    <div className="mx-auto w-full max-w-lg">
      <GlassPanel>
        <h1 className="text-2xl font-bold text-slate-900">Inscription agence</h1>
        <p className="mt-1 text-sm text-slate-600">
          Déjà inscrit ?{' '}
          <Link
            to="/connexion"
            className="cursor-pointer font-semibold text-teal-700 underline decoration-teal-400/70 underline-offset-2 hover:text-teal-900"
          >
            Connexion
          </Link>
        </p>

        <form onSubmit={onSubmit} className="mt-6 flex flex-col gap-4">
          <Input
            id="nom"
            name="nom"
            required
            minLength={2}
            label="Nom de l’agence"
            value={nom}
            onChange={(e) => setNom(e.target.value)}
          />
          <Input
            id="email"
            name="email"
            type="email"
            required
            label="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
          <Input
            id="password"
            name="password"
            type="password"
            required
            minLength={8}
            label="Mot de passe (min. 8 caractères)"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
          <Input
            id="telephone"
            name="telephone"
            label="Téléphone (optionnel)"
            value={telephone}
            onChange={(e) => setTelephone(e.target.value)}
          />
          <Input
            id="ville"
            name="ville"
            label="Ville (optionnel)"
            value={ville}
            onChange={(e) => setVille(e.target.value)}
          />
          <TextArea
            id="description"
            name="description"
            label="Description (optionnel)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />

          {error && (
            <p className="rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-800 ring-1 ring-rose-200" role="alert">
              {error}
            </p>
          )}

          <Button type="submit" disabled={pending} className="mt-2 w-full">
            {pending ? 'Envoi…' : 'Créer mon compte'}
          </Button>
        </form>
      </GlassPanel>
    </div>
    </div>
  )
}
