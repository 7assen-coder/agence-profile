export type AgencePublic = {
  id: number
  nom: string
  ville: string | null
  description: string | null
  logo: string | null
  statut: 'active' | 'suspendue' | 'en_attente' | string
  date_creation: string
}

export type AgencePrivate = AgencePublic & {
  email: string
  telephone: string | null
  adresse: string | null
  role: string
  date_maj: string
}

export type ApiErrorBody = {
  error: string
  details?: Record<string, string[]>
}
