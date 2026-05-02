# Gestion des places — module Flask

Partie du projet **Plateforme de réservation de bus**.  
Responsabilité : **génération des places** numérotées en base de données pour chaque bus.

---

## Périmètre

| Action | Endpoint | Appelé par |
|---|---|---|
| Générer les places d'un bus | `POST /places/generer` | Équipe gestion des bus |
| Lire les places d'un bus | `GET /places/<bus_id>` | Équipe affichage |
| Supprimer les places d'un bus | `DELETE /places/<bus_id>` | Interne / reconfiguration |

---

## Installation

```bash
# 1. Cloner et se placer dans le dossier
git clone <repo>
cd gestion_places

# 2. Créer un environnement virtuel
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows


# 3. Initialiser la base de données
mysql -u root -p < schema.sql
```

---

## Lancer l'application

```bash
python run.py
```

L'API tourne sur `http://localhost:5000`.

---

## API

### `POST /places/generer`

Génère les places pour un bus. Les capacités acceptées sont **15, 32 ou 60**.

**Corps JSON :**
```json
{ "bus_id": 3, "capacite": 15 }
```

**Réponse 201 :**
```json
{
  "bus_id": 3,
  "capacite": 15,
  "places_generees": 15,
  "message": "15 places générées avec succès pour le bus 3."
}
```

**Erreurs :**
- `400` — champs manquants ou types invalides
- `409` — places déjà générées pour ce bus
- `422` — capacité non autorisée (pas 15/32/60)

---

### `GET /places/<bus_id>`

Retourne la liste des places d'un bus.

**Réponse 200 :**
```json
{
  "bus_id": 3,
  "total": 15,
  "places": [
    { "id_place": 1, "numero_place": 1, "bus_id": 3 },
    { "id_place": 2, "numero_place": 2, "bus_id": 3 }
  ]
}
```

---

### `DELETE /places/<bus_id>`

Supprime toutes les places d'un bus (à utiliser avant de régénérer avec une autre capacité).

**Réponse 200 :**
```json
{ "bus_id": 3, "places_supprimees": 15, "message": "15 place(s) supprimée(s) pour le bus 3." }
```

---

## Tests

```bash
pytest tests/ -v
```

---

## Structure du projet

```
gestion_places/
├── app/
│   ├── __init__.py     # factory Flask
│   ├── database.py     # connexion MariaDB
│   ├── models.py       # logique métier
│   └── routes.py       # endpoints Blueprint
├── schema.sql          # DDL table place
├── run.py              # point d'entrée
└── .gitignore
```
