# Gestion Profil Agence — Module SaaS Trajets

Module **Flask + MySQL** du projet SaaS de réservation de transport interurbain.
Ce groupe gère tout ce qui concerne le **profil des agences de transport** :
inscription, connexion, gestion du profil, logo, statut (validation admin).

## Architecture du projet global

Le projet SaaS complet est divisé en modules indépendants :

| Module | Responsabilité |
|---|---|
| **Gestion Profil Agence** *(nous)* | Inscription, login, profil, logo, statut |
| Gestion Trajets | Publication des trajets (ville → ville, matin/après-midi) |
| Gestion Places | Génération des 12 places par trajet, disponibilité temps réel |
| Réservations | Blocage temporaire, confirmation |
| Paiements | Paiement en ligne, libération si échec |
| Admin | Supervision globale |

Chaque module expose une **API REST JSON** et partage la même base MySQL.

## Stack

- **Flask 3** + Blueprints
- **SQLAlchemy** + **Flask-Migrate** (Alembic)
- **PyMySQL** (driver MySQL)
- **Flask-JWT-Extended** (auth stateless)
- **Marshmallow** (validation des payloads)
- **Flask-CORS** (autoriser les autres modules)
- **Werkzeug** (hash des mots de passe)
- **pytest** (tests)
- **Jinja2** + HTML/CSS (sans JavaScript frontend) dans `app/templates/` et `app/static/css/` ; navigation et formulaires côté serveur (sessions signées)

## Démarrage rapide (API + site web)

Prérequis : **Python 3** avec dépendances installées (`pip install -r requirements.txt` dans un venv).

À la racine du dépôt :

```bash
npm install   # ou : bash scripts/dev.sh directement si vous préférez uniquement Python
npm run dev
```

Cela initialise la base SQLite (sans `.env`) dans **`instance/transport.db`**, injecte les **comptes de démonstration** (voir ci-dessous), puis lance **Flask** sur **http://127.0.0.1:5001** (`run.py`). Pages : hub `/` (connexion / inscription par rôle), `/espace/client`, `/espace/agence`, `/espace/admin`, annuaire `/agences`, JSON `/api/*`.

### Comptes de démonstration (seed automatique)

Après `bash scripts/dev.sh`, vous pouvez vous connecter sur le site :

| Rôle | Email | Mot de passe |
|------|--------|----------------|
| Client | `client.demo@transport.ma` | `ClientDemo2026!` |
| Agence | `agence.demo@transport.ma` | `AgenceDemo2026!` |
| Admin | `admin@transport.ma` | `AdminDemo2026!` |

L’admin n’a **pas** de formulaire d’inscription publique ; le compte est créé par le seed. Les JWT API agence utilisent désormais un identifiant `agence:<id>` ; login admin JSON : `{ "email", "password", "account_type": "admin" }`.

Sinon uniquement avec Python :

```bash
bash scripts/dev.sh
# ou après create_all une fois :
python run.py
```

**Sans npm** :

`source venv/bin/activate && python run.py`

**Rechargement auto Flask** : par défaut désactivé (un seul processus, moins de bruit dans le terminal). Pour le réactiver : `export FLASK_RELOADER=1` puis `python run.py`.

**Erreur « exit code 126 »** : souvent « permission denied » ou shell mal configuré. Vérifier `chmod +x scripts/dev.sh` ; lancer l’API avec `venv/bin/python run.py`.

## Structure

```
agence-profile/
├── scripts/
│   └── dev.sh               # Initialise SQLite puis Flask
├── package.json             # npm run dev (optionnel → dev.sh)
├── app/
│   ├── static/css/main.css  # Styles
│   ├── templates/          # Pages HTML (Jinja)
│   ├── __init__.py          # App factory
│   ├── config.py            # Config via .env
│   ├── extensions.py        # db, migrate, jwt, cors
│   ├── models/
│   │   └── domain.py         # Agence, Client, Admin, Villes, Bus, …
│   ├── routes/
│   │   ├── auth_routes.py   # /api/auth/*
│   │   ├── agence_routes.py # /api/agences/*
│   │   └── web_routes.py    # pages HTML (/, /agences, …)
│   ├── schemas/agence_schema.py  # Marshmallow
│   └── utils/
│       ├── auth.py          # Décorateurs JWT/role
│       └── validators.py    # Upload logo
├── tests/test_agence.py
├── schema.sql               # Schéma MySQL (partageable avec les autres groupes)
├── run.py
├── requirements.txt
└── .env.example
```

## Installation (backend seul)

```bash
git clone <repo-url>
cd agence-profile

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt

cp .env.example .env
# éditer .env avec tes infos MySQL (ou laisser absent pour SQLite via npm run dev)

mysql -u root -p < schema.sql

# (optionnel) migrations Alembic
flask db init
flask db migrate -m "init"
flask db upgrade

python run.py
```

L’API écoute sur `http://localhost:5001` par défaut (variables `FLASK_PORT` ou `PORT` pour changer).

## Endpoints

### Authentification

| Méthode | Route | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/register` | — | Inscription d'une nouvelle agence |
| POST | `/api/auth/login` | — | Connexion, renvoie un JWT |

### Profil (agence connectée)

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/agences/me` | JWT | Récupérer son profil |
| PUT | `/api/agences/me` | JWT | Mettre à jour son profil |
| PUT | `/api/agences/me/password` | JWT | Changer le mot de passe |
| POST | `/api/agences/me/logo` | JWT | Téléverser un logo (multipart) |
| DELETE | `/api/agences/me` | JWT | Supprimer son compte |

### Consultation publique

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/agences` | — | Liste des agences actives (`?ville=&page=&per_page=`) |
| GET | `/api/agences/<id>` | — | Profil public d'une agence |
| GET | `/api/agences/logos/<filename>` | — | Servir une image de logo |

### Admin

| Méthode | Route | Auth | Description |
|---|---|---|---|
| GET | `/api/agences/admin/all` | JWT admin | Toutes les agences |
| PUT | `/api/agences/admin/<id>/statut` | JWT admin | Changer le statut (active/suspendue/en_attente) |

## Exemples

### Inscription

```bash
curl -X POST http://localhost:5001/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "nom": "Agence Al Amal",
    "email": "contact@alamal.ma",
    "password": "motdepasse123",
    "telephone": "+22244112233",
    "ville": "Nouakchott",
    "description": "Transport quotidien Nouakchott ↔ Rosso"
  }'
```

### Login

```bash
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"contact@alamal.ma","password":"motdepasse123"}'
```

Réponse :
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "agence": { "id": 1, "nom": "Agence Al Amal", ... }
}
```

### Mettre à jour son profil

```bash
curl -X PUT http://localhost:5001/api/agences/me \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ville":"Rosso","description":"Nouvelle description"}'
```

### Upload logo

```bash
curl -X POST http://localhost:5001/api/agences/me/logo \
  -H "Authorization: Bearer $TOKEN" \
  -F "logo=@logo.png"
```

## Modèle de données

Voir [`schema.sql`](schema.sql). La table `agences` est **partagée** : les autres
modules pointeront vers `agences.id` comme clé étrangère (ex: `trajets.agence_id`).

## Intégration avec les autres modules

- **Module Trajets** : vérifie qu'une `agence.statut = 'active'` avant autorisation
  de publier un trajet. Utilise le JWT émis par ce module (même `JWT_SECRET_KEY`).
- **Module Admin** : utilise les routes `/api/agences/admin/*`.
- **CORS** : toutes les routes `/api/*` sont autorisées pour tous les origins
  (à restreindre en prod).

## Tests

```bash
pytest -q
```

Les tests utilisent SQLite en mémoire — aucun MySQL requis pour `pytest`.

## Sécurité

- Mots de passe hashés avec `werkzeug.security` (pbkdf2-sha256)
- JWT signé HS256, expiration 12h
- Validation stricte via Marshmallow
- Upload logo : extensions whitelistées, taille max 2 Mo, nom aléatoire
