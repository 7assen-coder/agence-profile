import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import * as api from '../api/client'
import type { AgencePublic } from '../types/agence'
import { GlassPanel } from '../components/ui/GlassPanel'
import { Input } from '../components/ui/Input'
import { Button } from '../components/ui/Button'
import { StatusBadge } from '../components/StatusBadge'

export function AgenciesPage() {
  const [villeDraft, setVilleDraft] = useState('')
  const [ville, setVille] = useState('')
  const [page, setPage] = useState(1)
  const [data, setData] = useState<{
    items: AgencePublic[]
    total: number
    pages: number
  } | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let cancelled = false
    ;(async () => {
      setError(null)
      try {
        const res = await api.listAgences({ page, per_page: 12, ville: ville || undefined })
        if (!cancelled) setData(res)
      } catch {
        if (!cancelled) setError('Impossible de charger les agences.')
      }
    })()
    return () => {
      cancelled = true
    }
  }, [page, ville])

  return (
    <div className="w-full px-6 py-12 sm:px-10 sm:py-14 lg:px-14">
    <div className="mx-auto flex w-full max-w-[100rem] flex-col gap-6">
      <div className="text-left">
        <h1 className="text-4xl font-bold tracking-tight text-slate-900 sm:text-5xl">Agences actives</h1>
        <p className="mt-2 text-lg text-slate-600 sm:text-xl">
          Liste publique — seules les agences au statut <strong>active</strong> apparaissent.
        </p>
      </div>

      <GlassPanel className="!py-4">
        <form
          className="flex flex-col gap-3 sm:flex-row sm:items-end"
          onSubmit={(e) => {
            e.preventDefault()
            setVille(villeDraft.trim())
            setPage(1)
          }}
        >
          <div className="min-w-[12rem] flex-1">
            <Input
              id="filtre-ville"
              label="Filtrer par ville"
              value={villeDraft}
              onChange={(e) => setVilleDraft(e.target.value)}
              placeholder="Ex. Nouakchott"
            />
          </div>
          <Button type="submit">Appliquer</Button>
        </form>
      </GlassPanel>

      {error && (
        <p className="rounded-lg bg-rose-50 px-3 py-2 text-sm text-rose-800 ring-1 ring-rose-200" role="alert">
          {error}
        </p>
      )}

      {data && (
        <>
          <p className="text-sm text-slate-600">
            {data.total} résultat{data.total > 1 ? 's' : ''}
          </p>
          <ul className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {data.items.map((a) => {
              const src = api.logoUrl(a.logo)
              return (
                <li key={a.id}>
                  <Link
                    to={`/agences/${a.id}`}
                    className="block cursor-pointer rounded-2xl border border-white/60 bg-white/70 p-5 shadow-[0_8px_30px_rgb(0,0,0,0.06)] backdrop-blur-xl transition duration-200 hover:border-teal-200 hover:shadow-md"
                  >
                    <div className="flex items-start gap-3">
                      {src ? (
                        <img
                          src={src}
                          alt=""
                          className="h-14 w-14 shrink-0 rounded-xl border border-slate-200 object-cover"
                        />
                      ) : (
                        <div className="flex h-14 w-14 shrink-0 items-center justify-center rounded-xl bg-teal-100 text-sm font-bold text-teal-800">
                          {a.nom.slice(0, 2).toUpperCase()}
                        </div>
                      )}
                      <div className="min-w-0 text-left">
                        <h2 className="font-semibold text-slate-900">{a.nom}</h2>
                        <p className="truncate text-sm text-slate-600">{a.ville ?? '—'}</p>
                        <div className="mt-2">
                          <StatusBadge statut={a.statut} />
                        </div>
                      </div>
                    </div>
                  </Link>
                </li>
              )
            })}
          </ul>

          {data.pages > 1 && (
            <div className="flex items-center justify-center gap-2">
              <Button
                type="button"
                variant="secondary"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
              >
                Précédent
              </Button>
              <span className="text-sm text-slate-600">
                Page {page} / {data.pages}
              </span>
              <Button
                type="button"
                variant="secondary"
                disabled={page >= data.pages}
                onClick={() => setPage((p) => p + 1)}
              >
                Suivant
              </Button>
            </div>
          )}
        </>
      )}
    </div>
    </div>
  )
}
