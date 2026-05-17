import type {
  Agence,
  Ville,
  Bus,
  Place,
  Trajet,
  Client,
  Paiement,
  Reservation,
} from '@/types';

// ============================================================
// Données de base
// ============================================================

export const agences: Agence[] = [
  { id_agence: 1, nom: 'TransSahara Express', telephone: '+222 36 00 11 22', email: 'contact@transsahara.mr', adresse: 'Avenue Gamal Abdel Nasser, Nouakchott' },
  { id_agence: 2, nom: 'Mauritanie Voyages', telephone: '+222 36 55 44 33', email: 'info@mauritanievoyages.mr', adresse: 'Rue Kennedy, Nouakchott' },
  { id_agence: 3, nom: 'Atlas Bus', telephone: '+222 36 77 88 99', email: 'contact@atlasbus.mr', adresse: 'Carrefour Madrid, Nouakchott' },
];

export const villes: Ville[] = [
  { id_ville: 1, nom: 'Nouakchott', region: 'Nouakchott-Nord' },
  { id_ville: 2, nom: 'Nouadhibou', region: 'Dakhlet Nouadhibou' },
  { id_ville: 3, nom: 'Rosso', region: 'Trarza' },
  { id_ville: 4, nom: 'Kiffa', region: 'Assaba' },
  { id_ville: 5, nom: 'Kaédi', region: 'Gorgol' },
  { id_ville: 6, nom: 'Zouérat', region: 'Tiris Zemmour' },
  { id_ville: 7, nom: 'Atar', region: 'Adrar' },
  { id_ville: 8, nom: 'Sélibabi', region: 'Guidimaka' },
];

export const bus: Bus[] = [
  { id_bus: 1, id_agence: 1, immatriculation: 'MR-NKT-001', capacite: 12 },
  { id_bus: 2, id_agence: 1, immatriculation: 'MR-NKT-002', capacite: 12 },
  { id_bus: 3, id_agence: 2, immatriculation: 'MR-MV-001', capacite: 12 },
  { id_bus: 4, id_agence: 2, immatriculation: 'MR-MV-002', capacite: 12 },
  { id_bus: 5, id_agence: 3, immatriculation: 'MR-AB-001', capacite: 12 },
  { id_bus: 6, id_agence: 3, immatriculation: 'MR-AB-002', capacite: 12 },
];

// Generate places for each bus (12 places each)
function generatePlaces(): Place[] {
  const result: Place[] = [];
  let id = 1;
  for (const b of bus) {
    for (let n = 1; n <= b.capacite; n++) {
      result.push({ id_place: id++, id_bus: b.id_bus, numero_place: n });
    }
  }
  return result;
}
export const places: Place[] = generatePlaces();

export const trajets: Trajet[] = [
  // --- Existing routes ---
  { id_trajet: 1, id_agence: 1, id_bus: 1, id_ville_depart: 1, id_ville_arrivee: 2, date_trajet: '2026-05-10', periode: 'matin', heure_depart: '07:00', heure_arrivee: '13:00', prix: 850 },
  { id_trajet: 2, id_agence: 1, id_bus: 2, id_ville_depart: 1, id_ville_arrivee: 2, date_trajet: '2026-05-10', periode: 'apres-midi', heure_depart: '14:00', heure_arrivee: '20:00', prix: 850 },
  { id_trajet: 3, id_agence: 2, id_bus: 3, id_ville_depart: 1, id_ville_arrivee: 3, date_trajet: '2026-05-10', periode: 'matin', heure_depart: '08:30', heure_arrivee: '11:30', prix: 450 },
  { id_trajet: 4, id_agence: 2, id_bus: 4, id_ville_depart: 1, id_ville_arrivee: 4, date_trajet: '2026-05-10', periode: 'matin', heure_depart: '06:00', heure_arrivee: '14:00', prix: 950 },
  { id_trajet: 5, id_agence: 3, id_bus: 5, id_ville_depart: 2, id_ville_arrivee: 1, date_trajet: '2026-05-10', periode: 'matin', heure_depart: '07:30', heure_arrivee: '13:30', prix: 850 },
  { id_trajet: 6, id_agence: 3, id_bus: 6, id_ville_depart: 1, id_ville_arrivee: 5, date_trajet: '2026-05-11', periode: 'apres-midi', heure_depart: '15:00', heure_arrivee: '21:00', prix: 700 },
  { id_trajet: 7, id_agence: 1, id_bus: 1, id_ville_depart: 1, id_ville_arrivee: 7, date_trajet: '2026-05-11', periode: 'matin', heure_depart: '06:30', heure_arrivee: '12:00', prix: 600 },
  { id_trajet: 8, id_agence: 2, id_bus: 3, id_ville_depart: 1, id_ville_arrivee: 6, date_trajet: '2026-05-12', periode: 'matin', heure_depart: '05:00', heure_arrivee: '15:00', prix: 1200 },

  // --- Kaédi ↔ Nouakchott — 07/05/2026 ---
  { id_trajet: 9,  id_agence: 2, id_bus: 4, id_ville_depart: 5, id_ville_arrivee: 1, date_trajet: '2026-05-07', periode: 'matin',     heure_depart: '05:30', heure_arrivee: '13:30', prix: 700 },
  { id_trajet: 10, id_agence: 2, id_bus: 4, id_ville_depart: 5, id_ville_arrivee: 1, date_trajet: '2026-05-07', periode: 'apres-midi', heure_depart: '14:00', heure_arrivee: '22:00', prix: 700 },
  { id_trajet: 11, id_agence: 2, id_bus: 3, id_ville_depart: 1, id_ville_arrivee: 5, date_trajet: '2026-05-07', periode: 'matin',     heure_depart: '06:00', heure_arrivee: '14:00', prix: 700 },
  { id_trajet: 12, id_agence: 2, id_bus: 3, id_ville_depart: 1, id_ville_arrivee: 5, date_trajet: '2026-05-07', periode: 'apres-midi', heure_depart: '15:00', heure_arrivee: '23:00', prix: 700 },

  // --- Kaédi ↔ Nouakchott — 08/05/2026 ---
  { id_trajet: 13, id_agence: 3, id_bus: 5, id_ville_depart: 5, id_ville_arrivee: 1, date_trajet: '2026-05-08', periode: 'matin',     heure_depart: '05:30', heure_arrivee: '13:30', prix: 700 },
  { id_trajet: 14, id_agence: 3, id_bus: 5, id_ville_depart: 5, id_ville_arrivee: 1, date_trajet: '2026-05-08', periode: 'apres-midi', heure_depart: '14:00', heure_arrivee: '22:00', prix: 700 },
  { id_trajet: 15, id_agence: 3, id_bus: 6, id_ville_depart: 1, id_ville_arrivee: 5, date_trajet: '2026-05-08', periode: 'matin',     heure_depart: '06:00', heure_arrivee: '14:00', prix: 700 },
  { id_trajet: 16, id_agence: 3, id_bus: 6, id_ville_depart: 1, id_ville_arrivee: 5, date_trajet: '2026-05-08', periode: 'apres-midi', heure_depart: '15:00', heure_arrivee: '23:00', prix: 700 },

  // --- Nouadhibou ↔ Sélibabi — 07/05/2026 ---
  { id_trajet: 17, id_agence: 1, id_bus: 1, id_ville_depart: 2, id_ville_arrivee: 8, date_trajet: '2026-05-07', periode: 'matin',     heure_depart: '06:00', heure_arrivee: '20:00', prix: 1500 },
  { id_trajet: 18, id_agence: 1, id_bus: 2, id_ville_depart: 8, id_ville_arrivee: 2, date_trajet: '2026-05-07', periode: 'matin',     heure_depart: '05:00', heure_arrivee: '19:00', prix: 1500 },

  // --- Nouadhibou ↔ Sélibabi — 08/05/2026 ---
  { id_trajet: 19, id_agence: 1, id_bus: 1, id_ville_depart: 2, id_ville_arrivee: 8, date_trajet: '2026-05-08', periode: 'matin',     heure_depart: '06:00', heure_arrivee: '20:00', prix: 1500 },
  { id_trajet: 20, id_agence: 1, id_bus: 2, id_ville_depart: 8, id_ville_arrivee: 2, date_trajet: '2026-05-08', periode: 'matin',     heure_depart: '05:00', heure_arrivee: '19:00', prix: 1500 },
];

export const clients: Client[] = [
  { id_client: 1, nom: 'Ould Ahmed', prenom: 'Mohamed', telephone: '+222 36 11 22 33', email: 'mohamed.ould@email.mr', cin: 'MR0012345' },
  { id_client: 2, nom: 'Mint Bah', prenom: 'Fatima', telephone: '+222 36 44 55 66', email: 'fatima.mint@email.mr', cin: 'MR0023456' },
  { id_client: 3, nom: 'Ould Cheikh', prenom: 'Abdallah', telephone: '+222 36 77 88 99', email: 'abdallah.cheikh@email.mr', cin: 'MR0034567' },
  { id_client: 4, nom: 'Mint Diallo', prenom: 'Mariam', telephone: '+222 36 00 11 22', email: 'mariam.diallo@email.mr', cin: 'MR0045678' },
  { id_client: 5, nom: 'Ould Salem', prenom: 'Sidi', telephone: '+222 36 33 44 55', email: 'sidi.salem@email.mr', cin: 'MR0056789' },
];

export const paiements: Paiement[] = [
  { id_paiement: 1, id_client: 1, montant: 850, date_paiement: '2026-05-01T09:15:00Z', mode_paiement: 'carte', statut: 'confirme' },
  { id_paiement: 2, id_client: 2, montant: 450, date_paiement: '2026-05-02T14:30:00Z', mode_paiement: 'mobile_money', statut: 'confirme' },
  { id_paiement: 3, id_client: 3, montant: 950, date_paiement: '2026-05-03T10:00:00Z', mode_paiement: 'virement', statut: 'confirme' },
  { id_paiement: 4, id_client: 4, montant: 700, date_paiement: '2026-05-04T16:45:00Z', mode_paiement: 'especes', statut: 'confirme' },
  { id_paiement: 5, id_client: 5, montant: 850, date_paiement: '2026-05-05T08:20:00Z', mode_paiement: 'carte', statut: 'confirme' },
];

export const reservations: Reservation[] = [
  { id_reservation: 1, id_client: 1, id_place: 1, id_trajet: 1, id_paiement: 1, date_reservation: '2026-05-01T09:00:00Z', statut: 'confirmee' },
  { id_reservation: 2, id_client: 2, id_place: 13, id_trajet: 3, id_paiement: 2, date_reservation: '2026-05-02T14:00:00Z', statut: 'confirmee' },
  { id_reservation: 3, id_client: 3, id_place: 25, id_trajet: 4, id_paiement: 3, date_reservation: '2026-05-03T09:45:00Z', statut: 'confirmee' },
  { id_reservation: 4, id_client: 4, id_place: 61, id_trajet: 6, id_paiement: 4, date_reservation: '2026-05-04T16:30:00Z', statut: 'confirmee' },
  { id_reservation: 5, id_client: 5, id_place: 2, id_trajet: 1, id_paiement: 5, date_reservation: '2026-05-05T08:00:00Z', statut: 'confirmee' },
  { id_reservation: 6, id_client: 1, id_place: 14, id_trajet: 3, id_paiement: null, date_reservation: '2026-05-06T10:00:00Z', statut: 'en_attente' },
];

// ============================================================
// Helper functions
// ============================================================

export function getAgenceById(id: number): Agence | undefined {
  return agences.find(a => a.id_agence === id);
}

export function getVilleById(id: number): Ville | undefined {
  return villes.find(v => v.id_ville === id);
}

export function getBusById(id: number): Bus | undefined {
  return bus.find(b => b.id_bus === id);
}

export function getPlacesByBusId(id_bus: number): Place[] {
  return places.filter(p => p.id_bus === id_bus);
}

export function getReservationsByTrajetId(id_trajet: number): Reservation[] {
  return reservations.filter(r => r.id_trajet === id_trajet && r.statut !== 'annulee');
}

export function getReservedPlaceIdsForTrajet(id_trajet: number): number[] {
  return getReservationsByTrajetId(id_trajet).map(r => r.id_place);
}
