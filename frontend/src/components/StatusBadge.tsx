import type { AgencePublic } from '../types/agence'

export function StatusBadge({ statut }: { statut: AgencePublic['statut'] }) {
  const map: Record<string, { label: string; className: string }> = {
    active: {
      label: 'Active',
      className: 'bg-emerald-100 text-emerald-800 ring-emerald-600/15',
    },
    en_attente: {
      label: 'En attente',
      className: 'bg-amber-100 text-amber-900 ring-amber-600/15',
    },
    suspendue: {
      label: 'Suspendue',
      className: 'bg-rose-100 text-rose-800 ring-rose-600/15',
    },
  }
  const s = map[statut] ?? {
    label: String(statut),
    className: 'bg-slate-100 text-slate-700 ring-slate-500/15',
  }
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ring-1 ring-inset ${s.className}`}
    >
      {s.label}
    </span>
  )
}
