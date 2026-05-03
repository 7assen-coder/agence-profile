# Groupe 20 – Module Statistiques
## Matricules : 251057 · 251092 · 251284

---

## Description
Module **Statistiques (revenus + taux de remplissage)** de la plateforme de réservation de transport.
Développé avec **Flask + MySQL**, expose une API REST JSON + un dashboard HTML intégré.

---

## Structure
```
stats_module/
├── app.py               # Backend Flask (API REST)
├── requirements.txt     # Dépendances Python
└── templates/
    └── dashboard.html   # Dashboard frontend
```

---

## Installation

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Variables d'environnement (optionnel, sinon valeurs par défaut)
export DB_HOST=localhost
export DB_USER=root
export DB_PASSWORD=votre_mdp
export DB_NAME=transport_reservation

# 3. Lancer le serveur
python app.py
# → http://localhost:5000
```

---

## Endpoints API REST

| Méthode | Route | Description |
|---------|-------|-------------|
| GET | `/api/stats/synthese` | KPIs globaux (dashboard cards) |
| GET | `/api/stats/revenus` | Revenu total (filtrable) |
| GET | `/api/stats/revenus/par-jour` | Revenus jour par jour |
| GET | `/api/stats/revenus/par-agence` | Revenus par agence |
| GET | `/api/stats/revenus/par-trajet` | Top trajets rentables |
| GET | `/api/stats/revenus/par-mode-paiement` | Répartition par mode de paiement |
| GET | `/api/stats/remplissage` | Taux de remplissage global |
| GET | `/api/stats/remplissage/par-trajet` | Taux par trajet |
| GET | `/api/stats/remplissage/par-agence` | Taux par agence |
| GET | `/api/stats/remplissage/par-periode` | Matin vs Après-midi |

### Paramètres de filtrage communs
| Paramètre | Type | Exemple |
|-----------|------|---------|
| `date_debut` | DATE | `2025-01-01` |
| `date_fin` | DATE | `2025-12-31` |
| `id_agence` | INT | `1` |

### Exemple de réponse
```json
GET /api/stats/synthese

{
  "success": true,
  "data": {
    "revenu_total": 1250000,
    "revenu_ce_mois": 320000,
    "nb_reservations": 87,
    "taux_remplissage": 72.5
  }
}
```

---

## Formule taux de remplissage

```
taux = (places_confirmées / capacité_totale_bus) × 100
```

- `places_confirmées` = réservations avec `statut = 'confirmee'`
- `capacité_totale_bus` = `bus.capacite` (12 par défaut)

---

## Dépendances avec les autres modules

| Module fournisseur | Ce que nous consommons |
|-------------------|------------------------|
| Groupe 6 (Création trajets) | Table `trajets` |
| Groupe 8 (Bus) | Table `bus`, `places` |
| Groupe 13 (Réservation) | Table `reservations` |
| Groupe 16 (Paiement) | Table `paiements` |
| Groupe 4 (Villes) | Table `villes` |

> Notre module est **100 % lecture** (SELECT uniquement). Il n'écrit dans aucune table.

---

## Base de données utilisée
La base commune `transport_reservation` définie dans `transport_reservation.sql`.
Tables consultées : `agences`, `trajets`, `bus`, `places`, `reservations`, `paiements`, `villes`.
