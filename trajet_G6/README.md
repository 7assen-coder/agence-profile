# Transport Réservation — Système de Gestion des Trajets

Application web de gestion de réservations de transport en commun, développée avec Flask et MySQL. Elle permet aux agences de transport de créer et gérer des trajets entre villes.

---

## Table des matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies utilisées](#technologies-utilisées)
- [Structure du projet](#structure-du-projet)
- [Prérequis](#prérequis)
- [Installation](#installation)
- [Base de données](#base-de-données)
- [Lancer l'application](#lancer-lapplication)
- [Pages disponibles](#pages-disponibles)

---

## Aperçu

Ce projet est un système SaaS de gestion de trajets de transport. Il permet de :

- Créer des trajets avec sélection d'agence, de bus, de villes de départ/arrivée, de date, d'horaire et de prix
- Lister tous les trajets enregistrés dans un tableau clair et lisible
- Naviguer facilement entre la liste et le formulaire de création

---

## Fonctionnalités

- Création de trajets (agence, bus, villes, date, période, horaires, prix)
- Liste des trajets avec affichage des noms complets (villes, agences, bus)
- Badges visuels par période (Matin / Après-midi)
- Aperçu de la route en temps réel dans le formulaire
- Interface responsive avec scroll horizontal sur mobile
- Navigation fluide entre les pages

---

## Technologies utilisées

| Couche          | Technologie                      |
|-----------------|----------------------------------|
| Backend         | Python 3 / Flask                 |
| Base de données | MySQL                            |
| Frontend        | HTML5, CSS3, JavaScript vanilla  |
| Polices         | Google Fonts — DM Sans, DM Mono  |
| Templating      | Jinja2                           |

---

## Structure du projet

```
transport-reservation/
│
├── app.py                  # Application Flask principale
│
├── templates/
│   ├── index.html          # Formulaire de création de trajet
│   └── liste_trajets.html  # Liste des trajets
│
├── static/
│   ├── style.css           # Styles globaux
│   └── script.js           # Interactions côté client
│
└── README.md
```

---

## Prérequis

- Python 3.8+
- MySQL Server
- pip

---

## Installation

### 1. Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/transport-reservation.git
cd transport-reservation
```

### 2. Créer un environnement virtuel

```bash
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows
```

### 3. Installer les dépendances

```bash
pip install flask mysql-connector-python
```

### 4. Configurer la connexion à la base de données

Dans `app.py`, modifiez la fonction `get_connection()` avec vos identifiants MySQL :

```python
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",         # votre utilisateur MySQL
        password="",         # votre mot de passe MySQL
        database="trajets_saas"
    )
```

---

## Base de données

### Créer la base de données

```sql
CREATE DATABASE trajets_saas;
USE trajets_saas;
```

### Tables requises

#### Table `agences`

```sql
CREATE TABLE agences (
    id_agence INT AUTO_INCREMENT PRIMARY KEY,
    nom       VARCHAR(100) NOT NULL
);
```

#### Table `bus`

```sql
CREATE TABLE bus (
    id_bus    INT AUTO_INCREMENT PRIMARY KEY,
    label     VARCHAR(100) NOT NULL,
    nb_places INT NOT NULL
);
```

#### Table `villes`

```sql
CREATE TABLE villes (
    id_ville INT AUTO_INCREMENT PRIMARY KEY,
    nom      VARCHAR(100) NOT NULL
);
```

#### Table `trajets`

```sql
CREATE TABLE trajets (
    id_trajet        INT AUTO_INCREMENT PRIMARY KEY,
    id_agence        INT NOT NULL,
    id_bus           INT NOT NULL,
    id_ville_depart  INT NOT NULL,
    id_ville_arrivee INT NOT NULL,
    date_trajet      DATE NOT NULL,
    periode          ENUM('matin', 'apres-midi') NOT NULL,
    heure_depart     TIME,
    heure_arrivee    TIME,
    prix             DECIMAL(10, 2) NOT NULL,

    CONSTRAINT fk_trajet_agence  FOREIGN KEY (id_agence)        REFERENCES agences(id_agence) ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_trajet_bus     FOREIGN KEY (id_bus)           REFERENCES bus(id_bus)        ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_trajet_depart  FOREIGN KEY (id_ville_depart)  REFERENCES villes(id_ville)   ON DELETE RESTRICT ON UPDATE CASCADE,
    CONSTRAINT fk_trajet_arrivee FOREIGN KEY (id_ville_arrivee) REFERENCES villes(id_ville)   ON DELETE RESTRICT ON UPDATE CASCADE
);
```

### Données de test (optionnel)

```sql
INSERT INTO agences (nom) VALUES ('Sahel Express'), ('Trans Mauritanie'), ('Adrar Lines');

INSERT INTO bus (label, nb_places) VALUES ('Bus A1', 40), ('Bus B2', 30), ('Minibus C3', 20);

INSERT INTO villes (nom) VALUES ('Nouakchott'), ('Nouadhibou'), ('Rosso'), ('Kiffa'), ('Zouerate');
```

---

## Lancer l'application

```bash
python app.py
```

L'application sera disponible sur : http://localhost:5000

---

## Pages disponibles

| URL               | Méthode | Description                 |
|-------------------|---------|-----------------------------|
| `/` ou `/trajets` | GET     | Liste de tous les trajets   |
| `/add_trajet`     | GET     | Formulaire de création      |
| `/add_trajet`     | POST    | Soumettre un nouveau trajet |

---

## Auteur

Projet réalisé dans le cadre d'un système de gestion de transport en commun.