import { useEffect, useState } from 'react'
import { Link, useParams } from 'react-router-dom'
import * as api from '../api/client'
import type { AgencePublic } from '../types/agence'
import { GlassPanel } from '../components/ui/GlassPanel'
import { StatusBadge } from '../components/StatusBadge'

export function AgencyDetailPage() {
  const { id } = useParams<{ id: string }>()
  const [agence, setAgence] = useState<AgencePublic | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    if (!id) return
    let cancelled = false
    ;(async () => {
      setError(null)
      try {
        const res = await api.getAgencePublic(Number(id))
        if (!cancelled) setAgence(res.agence)
      } catch {
        if (!cancelled) {
          setAgence(null)
          setError('Agence introuvable ou non publiée.')
        }
      }
    })()
    return () => {
      cancelled = true
    }
  }, [id])

  if (error) {
    return (
      <div className="w-full px-6 py-12 sm:px-10 sm:py-14 lg:px-14">
        <GlassPanel className="mx-auto max-w-2xl">
          <p className="text-rose-800">{error}</p>
          <Link
            to="/agences"
            className="mt-4 inline-block cursor-pointer font-semibold text-teal-700 underline"
          >
            Retour à la liste
          </Link>
        </GlassPanel>
      </div>
    )
  }

  if (!agence) {
    return (
      <div className="w-full px-6 py-20 text-center text-xl text-slate-600 sm:px-10">
        Chargement…
      </div>
    )
  }

  const src = api.logoUrl(agence.logo)

  return (
    <div className="w-full px-6 py-12 sm:px-10 sm:py-14 lg:px-14">
    <div className="mx-auto max-w-2xl">
      <Link
        to="/agences"
        className="mb-6 inline-flex cursor-pointer text-sm font-semibold text-teal-700 hover:text-teal-900"
      >
        ← Agences
      </Link>
      <GlassPanel>
        <div className="flex flex-col gap-6 sm:flex-row sm:items-start">
          {src ? (
            <img
              src={src}
              alt=""
              className="h-32 w-32 shrink-0 rounded-2xl border border-slate-200 object-cover shadow-inner"
            />
          ) : (
            <div className="flex h-32 w-32 shrink-0 items-center justify-center rounded-2xl bg-teal-100 text-2xl font-bold text-teal-800">
              {agence.nom.slice(0, 2).toUpperCase()}
            </div>
          )}
          <div className="min-w-0 flex-1 text-left">
            <h1 className="text-2xl font-bold text-slate-900">{agence.nom}</h1>
            <p className="mt-1 text-slate-600">{agence.ville ?? 'Ville non renseignée'}</p>
            <div className="mt-3">
              <StatusBadge statut={agence.statut} />
            </div>
            {agence.description && (
              <p className="mt-4 whitespace-pre-wrap text-slate-700">{agence.description}</p>
            )}
            <p className="mt-4 text-xs text-slate-500">
              Création : {new Date(agence.date_creation).toLocaleDateString('fr-FR')}
            </p>
          </div>
        </div>
      </GlassPanel>
    </div>
    </div>
  )
}
