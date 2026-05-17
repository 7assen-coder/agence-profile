import { type FormEvent, useState } from 'react'
import { useAuth } from '../context/AuthContext'
import * as api from '../api/client'
import { ApiError } from '../api/client'
import type { AgencePrivate } from '../types/agence'
import { GlassPanel } from '../components/ui/GlassPanel'
import { Input, TextArea } from '../components/ui/Input'
import { Button } from '../components/ui/Button'
import { StatusBadge } from '../components/StatusBadge'

function ProfileEditor({
  agence,
  onSaved,
}: {
  agence: AgencePrivate
  onSaved: (a: AgencePrivate) => void
}) {
  const [nom, setNom] = useState(agence.nom)
  const [telephone, setTelephone] = useState(agence.telephone ?? '')
  const [adresse, setAdresse] = useState(agence.adresse ?? '')
  const [ville, setVille] = useState(agence.ville ?? '')
  const [description, setDescription] = useState(agence.description ?? '')
  const [pending, setPending] = useState(false)
  const [err, setErr] = useState<string | null>(null)

  async function onSaveProfile(e: FormEvent) {
    e.preventDefault()
    setErr(null)
    setPending(true)
    try {
      const { agence: updated } = await api.updateMe({
        nom,
        telephone: telephone || undefined,
        adresse: adresse || undefined,
        ville: ville || undefined,
        description: description || undefined,
      })
      onSaved(updated)
    } catch (e2) {
      if (e2 instanceof ApiError) setErr(e2.message)
      else setErr('Erreur réseau.')
    } finally {
      setPending(false)
    }
  }

  return (
    <GlassPanel className="lg:col-span-2">
      <div className="flex flex-wrap items-start justify-between gap-4 border-b border-slate-200/80 pb-4">
        <div>
          <h2 className="text-lg font-semibold text-slate-900">Profil</h2>
          <p className="text-sm text-slate-600">{agence.email}</p>
        </div>
        <StatusBadge statut={agence.statut} />
      </div>

      <form onSubmit={onSaveProfile} className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="sm:col-span-2">
          <Input id="nom" label="Nom" value={nom} onChange={(e) => setNom(e.target.value)} required minLength={2} />
        </div>
        <Input
          id="telephone"
          label="Téléphone"
          value={telephone}
          onChange={(e) => setTelephone(e.target.value)}
        />
        <Input id="ville" label="Ville" value={ville} onChange={(e) => setVille(e.target.value)} />
        <div className="sm:col-span-2">
          <Input
            id="adresse"
            label="Adresse"
            value={adresse}
            onChange={(e) => setAdresse(e.target.value)}
          />
        </div>
        <div className="sm:col-span-2">
          <TextArea
            id="description"
            label="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
          />
        </div>
        {err && (
          <p className="sm:col-span-2 rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-800 ring-1 ring-rose-200" role="alert">
            {err}
          </p>
        )}
        <div className="sm:col-span-2">
          <Button type="submit" disabled={pending}>
            {pending ? 'Enregistrement…' : 'Enregistrer le profil'}
          </Button>
        </div>
      </form>
    </GlassPanel>
  )
}

export function DashboardPage() {
  const { agence, refreshAgence, setAgence } = useAuth()

  const [ancien, setAncien] = useState('')
  const [nouveau, setNouveau] = useState('')
  const [msg, setMsg] = useState<string | null>(null)
  const [err, setErr] = useState<string | null>(null)
  const [pending, setPending] = useState(false)
  const [logoPending, setLogoPending] = useState(false)

  if (!agence) {
    return (
      <div className="w-full px-6 py-14 sm:px-10 sm:py-16 lg:px-14">
        <div className="mx-auto max-w-7xl py-12 text-center text-slate-600">
          Session invalide. Reconnectez-vous.
        </div>
      </div>
    )
  }

  async function onChangePassword(e: FormEvent) {
    e.preventDefault()
    setErr(null)
    setMsg(null)
    setPending(true)
    try {
      await api.changePassword({
        ancien_password: ancien,
        nouveau_password: nouveau,
      })
      setAncien('')
      setNouveau('')
      setMsg('Mot de passe mis à jour.')
    } catch (e2) {
      if (e2 instanceof ApiError) {
        if (e2.body?.error === 'ancien_password_incorrect') {
          setErr('Ancien mot de passe incorrect.')
        } else setErr(e2.message)
      } else setErr('Erreur réseau.')
    } finally {
      setPending(false)
    }
  }

  async function onLogoChange(file: File | null) {
    if (!file) return
    setErr(null)
    setMsg(null)
    setLogoPending(true)
    try {
      await api.uploadLogo(file)
      await refreshAgence()
      setMsg('Logo mis à jour.')
    } catch (e2) {
      if (e2 instanceof ApiError) {
        if (e2.body?.error === 'extension_non_autorisee') {
          setErr('Format non autorisé (png, jpg, jpeg, webp).')
        } else if (e2.body?.error === 'file_too_large') setErr('Fichier trop volumineux.')
        else setErr(e2.message)
      } else setErr('Erreur réseau.')
    } finally {
      setLogoPending(false)
    }
  }

  function handleProfileSaved(updated: AgencePrivate) {
    setAgence(updated)
    setMsg('Profil enregistré.')
    setErr(null)
  }

  const logoSrc = api.logoUrl(agence.logo)

  return (
    <div className="w-full px-6 py-12 sm:px-10 sm:py-14 lg:px-14">
    <div className="mx-auto flex w-full max-w-[90rem] flex-col gap-6">
      <div className="text-left">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">Mon compte</h1>
        <p className="mt-2 text-lg text-slate-600 sm:text-xl">
          Gestion du profil agence — API{' '}
          <code className="rounded bg-slate-100 px-1 text-sm">/api/agences/me</code>
        </p>
      </div>

      {(msg || err) && (
        <div
          className={`rounded-xl px-4 py-3 text-sm ${
            err
              ? 'bg-rose-50 text-rose-900 ring-1 ring-rose-200'
              : 'bg-emerald-50 text-emerald-900 ring-1 ring-emerald-200'
          }`}
          role={err ? 'alert' : 'status'}
        >
          {err ?? msg}
        </div>
      )}

      <div className="grid gap-6 lg:grid-cols-3">
        <ProfileEditor
          key={agence.date_maj}
          agence={agence}
          onSaved={handleProfileSaved}
        />

        <div className="flex flex-col gap-6">
          <GlassPanel>
            <h2 className="text-lg font-semibold text-slate-900">Logo</h2>
            <p className="mt-1 text-sm text-slate-600">PNG, JPG, JPEG ou WebP — max 2 Mo.</p>
            <div className="mt-4 flex flex-col items-center gap-3">
              {logoSrc ? (
                <img
                  src={logoSrc}
                  alt=""
                  className="h-24 w-24 rounded-2xl border border-slate-200 object-cover shadow-inner"
                />
              ) : (
                <div className="flex h-24 w-24 items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50 text-xs text-slate-500">
                  Aucun logo
                </div>
              )}
              <label className="cursor-pointer rounded-xl border border-slate-200 bg-white px-4 py-2 text-sm font-medium text-slate-800 shadow-sm transition hover:border-teal-400 hover:text-teal-900">
                {logoPending ? 'Envoi…' : 'Choisir un fichier'}
                <input
                  type="file"
                  accept="image/png,image/jpeg,image/webp"
                  className="sr-only"
                  disabled={logoPending}
                  onChange={(e) => onLogoChange(e.target.files?.[0] ?? null)}
                />
              </label>
            </div>
          </GlassPanel>

          <GlassPanel>
            <h2 className="text-lg font-semibold text-slate-900">Mot de passe</h2>
            <form onSubmit={onChangePassword} className="mt-4 flex flex-col gap-3">
              <Input
                id="ancien"
                type="password"
                autoComplete="current-password"
                label="Ancien mot de passe"
                value={ancien}
                onChange={(e) => setAncien(e.target.value)}
                required
              />
              <Input
                id="nouveau"
                type="password"
                autoComplete="new-password"
                label="Nouveau mot de passe"
                value={nouveau}
                onChange={(e) => setNouveau(e.target.value)}
                required
                minLength={8}
              />
              <Button type="submit" variant="secondary" disabled={pending}>
                Mettre à jour le mot de passe
              </Button>
            </form>
          </GlassPanel>
        </div>
      </div>
    </div>
    </div>
  )
}
