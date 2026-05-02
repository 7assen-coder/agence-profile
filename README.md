# Gestion des places — module Flask

Partie du projet **Plateforme de réservation de bus**.  
Responsabilité : **génération des places** numérotées en base de données pour chaque bus.

---

## Périmètre

| Action | Endpoint | Appelé par |
|---|---|---|
| Générer les places d'un bus | `POST /places/generer` | Équipe gestion des bus |
| Lire les places d'un bus | `GET /places/<id_bus>` | Équipe affichage |
| Supprimer les places d'un bus | `DELETE /places/<id_bus>` | Interne / reconfiguration |

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

Génère les places pour un bus. Les capacités acceptées sont **12, 32 ou 60**.

**Corps JSON :**
```json
{ "id_bus": 3, "capacite": 12 }
```

**Réponse 201 :**
```json
{
  "id_bus": 3,
  "capacite": 12,
  "places_generees": 12,
  "message": "12 places générées avec succès pour le bus 3."
}
```

**Erreurs :**
- `400` — champs manquants ou types invalides
- `409` — places déjà générées pour ce bus
- `422` — capacité non autorisée (pas 15/32/60)

---

### `GET /places/<id_bus>`

Retourne la liste des places d'un bus.

**Réponse 200 :**
```json
{
  "id_bus": 3,
  "total": 12,
  "places": [
    { "id_place": 1, "numero_place": 1, "id_bus": 3 },
    { "id_place": 2, "numero_place": 2, "id_bus": 3 }
  ]
}
```

---

### `DELETE /places/<id_bus>`

Supprime toutes les places d'un bus (à utiliser avant de régénérer avec une autre capacité).

**Réponse 200 :**
```json
{ "id_bus": 3, "places_supprimees": 12, "message": "12 place(s) supprimée(s) pour le bus 3." }
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
│   ├── database.py     # connexion MariaDB ou MYSQL
│   ├── models.py       # logique métier
│   └── routes.py       # endpoints Blueprint
├── schema.sql          # DDL table place
├── run.py              # point d'entrée
└── .gitignore
```
