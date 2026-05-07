// Types correspondant au schéma de base de données transport_reservation

export interface Agence {
  id_agence: number;
  nom: string;
  telephone: string;
  email: string;
  adresse: string;
}

export interface Ville {
  id_ville: number;
  nom: string;
  region: string;
}

export interface Bus {
  id_bus: number;
  id_agence: number;
  immatriculation: string;
  capacite: number;
}

export interface Place {
  id_place: number;
  id_bus: number;
  numero_place: number;
  statut?: 'disponible' | 'reservee' | 'selectionnee' | 'occupee';
}

export interface Trajet {
  id_trajet: number;
  id_agence: number;
  id_bus: number;
  id_ville_depart: number;
  id_ville_arrivee: number;
  date_trajet: string;
  periode: 'matin' | 'apres-midi';
  heure_depart: string;
  heure_arrivee: string;
  prix: number;
}

export interface Client {
  id_client: number;
  nom: string;
  prenom: string;
  telephone: string;
  email: string;
  cin: string;
}

export type ModePaiement = 'especes' | 'carte' | 'mobile_money' | 'virement';
export type StatutPaiement = 'en_attente' | 'confirme' | 'echoue' | 'rembourse';

export interface Paiement {
  id_paiement: number;
  id_client: number;
  montant: number;
  date_paiement: string;
  mode_paiement: ModePaiement;
  statut: StatutPaiement;
}

export type StatutReservation = 'en_attente' | 'confirmee' | 'annulee';

export interface Reservation {
  id_reservation: number;
  id_client: number;
  id_place: number;
  id_trajet: number;
  id_paiement: number | null;
  date_reservation: string;
  statut: StatutReservation;
}

// Types composites pour l'UI

export interface TrajetComplet extends Trajet {
  agence?: Agence;
  ville_depart?: Ville;
  ville_arrivee?: Ville;
  bus?: Bus;
  places_disponibles?: number;
}

export interface ReservationComplet extends Reservation {
  client?: Client;
  place?: Place;
  trajet?: TrajetComplet;
  paiement?: Paiement;
}

export interface SearchParams {
  id_ville_depart: number;
  id_ville_arrivee: number;
  date_trajet: string;
  periode?: 'matin' | 'apres-midi' | 'tous';
}

export interface BookingFlow {
  step: 'search' | 'results' | 'seats' | 'payment' | 'ticket';
  selectedTrajet?: TrajetComplet;
  selectedPlace?: Place;
  client?: Partial<Client>;
  paiement?: Partial<Paiement>;
  reservation?: ReservationComplet;
}
