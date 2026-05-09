/**
 * api.ts — Appels vers le backend Flask (http://localhost:5003)
 * Remplace l'ancienne version qui utilisait mockData.
 */

import type { TrajetComplet, Place, Reservation, SearchParams, Ville } from '@/types';

const API_BASE = '/api';

// ── Helpers ────────────────────────────────────────────────────────────────

async function apiFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.message || err.error || `Erreur ${res.status}`);
  }
  return res.json();
}

// ── Villes ─────────────────────────────────────────────────────────────────

export async function getVilles(): Promise<Ville[]> {
  // Les villes viennent du module Trajets (autre groupe).
  // En attendant, on utilise la liste statique mauritanienne.
  return [
    { id_ville: 1, nom: 'Nouakchott',  region: 'Nouakchott-Nord' },
    { id_ville: 2, nom: 'Nouadhibou',  region: 'Dakhlet Nouadhibou' },
    { id_ville: 3, nom: 'Rosso',       region: 'Trarza' },
    { id_ville: 4, nom: 'Kiffa',       region: 'Assaba' },
    { id_ville: 5, nom: 'Kaédi',       region: 'Gorgol' },
    { id_ville: 6, nom: 'Zouérat',     region: 'Tiris Zemmour' },
    { id_ville: 7, nom: 'Atar',        region: 'Adrar' },
    { id_ville: 8, nom: 'Sélibabi',    region: 'Guidimaka' },
  ];
}

// ── Trajets ────────────────────────────────────────────────────────────────
// Le module Trajets expose GET /api/trajets?ville_depart=X&ville_arrivee=Y&date=Z
// Si ce module n'est pas encore prêt, on retourne une liste vide.

export async function searchTrajets(params: SearchParams): Promise<TrajetComplet[]> {
  try {
    const qs = new URLSearchParams({
      ville_depart:  String(params.id_ville_depart),
      ville_arrivee: String(params.id_ville_arrivee),
      date:          params.date_trajet,
      ...(params.periode && params.periode !== 'tous' ? { periode: params.periode } : {}),
    });
    return await apiFetch<TrajetComplet[]>(`/trajets?${qs}`);
  } catch {
    // Module Trajets pas encore disponible → liste vide
    console.warn('Module Trajets non disponible, aucun trajet retourné.');
    return [];
  }
}

// ── Places ─────────────────────────────────────────────────────────────────
// GET /api/reservations/trajet/:id/places  → notre module Flask

export async function getPlacesForTrajet(trajetId: number): Promise<Place[]> {
  const data = await apiFetch<{ places: { numero: number; statut: string }[] }>(
    `/reservations/trajet/${trajetId}/places`
  );
  return data.places.map((p) => ({
    id_place:     p.numero,   // on utilise le numéro comme id
    id_bus:       0,
    numero_place: p.numero,
    statut:       p.statut === 'disponible' ? 'disponible'
                : p.statut === 'confirmee'  ? 'reservee'
                : p.statut === 'en_attente' ? 'reservee'   // bloquée temporairement
                : 'disponible',
  }));
}

// ── Créer une réservation ──────────────────────────────────────────────────
// POST /api/reservations

interface CreerReservationPayload {
  trajet_id:        number;
  client_nom:       string;
  client_email:     string;
  client_telephone?: string;
  numero_place:     number;
}

export async function creerReservation(payload: CreerReservationPayload): Promise<Reservation> {
  const data = await apiFetch<{ reservation: {
    id:               number;
    trajet_id:        number;
    numero_place:     number;
    statut:           string;
    date_expiration:  string | null;
    date_creation:    string;
  } }>('/reservations', {
    method: 'POST',
    body: JSON.stringify(payload),
  });

  // Adapte la réponse Flask au type Reservation de l'UI
  return {
    id_reservation:   data.reservation.id,
    id_client:        0,
    id_place:         data.reservation.numero_place,
    id_trajet:        data.reservation.trajet_id,
    id_paiement:      null,
    date_reservation: data.reservation.date_creation,
    statut:           data.reservation.statut as Reservation['statut'],
  };
}

// ── Confirmer une réservation ──────────────────────────────────────────────
// PUT /api/reservations/:id/confirmer  (appelé par le module Paiement)

export async function confirmerReservation(
  reservationId: number,
  paiementRef: string
): Promise<Reservation> {
  const data = await apiFetch<{ reservation: {
    id:            number;
    trajet_id:     number;
    numero_place:  number;
    statut:        string;
    date_creation: string;
  } }>(`/reservations/${reservationId}/confirmer`, {
    method: 'PUT',
    body: JSON.stringify({ paiement_ref: paiementRef }),
  });

  return {
    id_reservation:   data.reservation.id,
    id_client:        0,
    id_place:         data.reservation.numero_place,
    id_trajet:        data.reservation.trajet_id,
    id_paiement:      null,
    date_reservation: data.reservation.date_creation,
    statut:           data.reservation.statut as Reservation['statut'],
  };
}

// ── Annuler une réservation ────────────────────────────────────────────────
// DELETE /api/reservations/:id

export async function annulerReservation(reservationId: number): Promise<void> {
  await apiFetch(`/reservations/${reservationId}`, { method: 'DELETE' });
}

// ── Lister les réservations (admin) ───────────────────────────────────────
// GET /api/reservations

export async function getReservations(filters?: {
  statut?: string;
  trajet_id?: number;
}): Promise<Reservation[]> {
  const qs = new URLSearchParams();
  if (filters?.statut)    qs.set('statut',    filters.statut);
  if (filters?.trajet_id) qs.set('trajet_id', String(filters.trajet_id));

  const data = await apiFetch<{ items: {
    id:            number;
    trajet_id:     number;
    numero_place:  number;
    statut:        string;
    date_creation: string;
  }[] }>(`/reservations?${qs}`);

  return data.items.map((r) => ({
    id_reservation:   r.id,
    id_client:        0,
    id_place:         r.numero_place,
    id_trajet:        r.trajet_id,
    id_paiement:      null,
    date_reservation: r.date_creation,
    statut:           r.statut as Reservation['statut'],
  }));
}
