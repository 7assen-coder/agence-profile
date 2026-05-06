-- ============================================================
--  BASE : Plateforme de réservation transport (SQLAlchemy aligné)
-- ============================================================

CREATE DATABASE IF NOT EXISTS transport_reservation
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE transport_reservation;

-- ------------------------------------------------------------
-- Extensions auth (non présentes dans le MCD brut)
-- ------------------------------------------------------------
-- password_hash, statut, logo, ville, description, dates sur agences
-- password_hash sur clients
-- table administrateurs

CREATE TABLE IF NOT EXISTS agences (
  id_agence     INT AUTO_INCREMENT PRIMARY KEY,
  nom           VARCHAR(100) NOT NULL,
  telephone     VARCHAR(20) NULL,
  email         VARCHAR(100) NOT NULL UNIQUE,
  adresse       VARCHAR(200) NULL,
  password_hash VARCHAR(255) NOT NULL,
  statut        ENUM('active','suspendue','en_attente') NOT NULL DEFAULT 'en_attente',
  logo          VARCHAR(255) NULL,
  ville         VARCHAR(80) NULL,
  description   TEXT NULL,
  date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_maj      DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS villes (
  id_ville INT AUTO_INCREMENT PRIMARY KEY,
  nom      VARCHAR(100) NOT NULL,
  region   VARCHAR(100) NULL
);

CREATE TABLE IF NOT EXISTS bus (
  id_bus          INT AUTO_INCREMENT PRIMARY KEY,
  id_agence       INT NOT NULL,
  immatriculation VARCHAR(20) NOT NULL UNIQUE,
  capacite        INT NOT NULL DEFAULT 12,
  CONSTRAINT fk_bus_agence FOREIGN KEY (id_agence)
    REFERENCES agences(id_agence) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS places (
  id_place     INT AUTO_INCREMENT PRIMARY KEY,
  id_bus       INT NOT NULL,
  numero_place TINYINT NOT NULL,
  CONSTRAINT fk_place_bus FOREIGN KEY (id_bus)
    REFERENCES bus(id_bus) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT chk_numero_place CHECK (numero_place BETWEEN 1 AND 12),
  CONSTRAINT uq_place_bus UNIQUE (id_bus, numero_place)
);

CREATE TABLE IF NOT EXISTS trajets (
  id_trajet        INT AUTO_INCREMENT PRIMARY KEY,
  id_agence        INT NOT NULL,
  id_bus           INT NOT NULL,
  id_ville_depart  INT NOT NULL,
  id_ville_arrivee INT NOT NULL,
  date_trajet      DATE NOT NULL,
  periode          ENUM('matin','apres-midi') NOT NULL,
  heure_depart     TIME NULL,
  heure_arrivee    TIME NULL,
  prix             DECIMAL(10, 2) NOT NULL,
  CONSTRAINT fk_trajet_agence   FOREIGN KEY (id_agence) REFERENCES agences(id_agence),
  CONSTRAINT fk_trajet_bus      FOREIGN KEY (id_bus) REFERENCES bus(id_bus),
  CONSTRAINT fk_trajet_depart   FOREIGN KEY (id_ville_depart) REFERENCES villes(id_ville),
  CONSTRAINT fk_trajet_arrivee  FOREIGN KEY (id_ville_arrivee) REFERENCES villes(id_ville)
);

CREATE TABLE IF NOT EXISTS clients (
  id_client     INT AUTO_INCREMENT PRIMARY KEY,
  nom           VARCHAR(100) NOT NULL,
  prenom        VARCHAR(100) NOT NULL,
  telephone     VARCHAR(20) NULL,
  email         VARCHAR(100) NOT NULL UNIQUE,
  cin           VARCHAR(20) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  date_creation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS administrateurs (
  id_admin      INT AUTO_INCREMENT PRIMARY KEY,
  email         VARCHAR(100) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  nom           VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS paiements (
  id_paiement   INT AUTO_INCREMENT PRIMARY KEY,
  id_client     INT NOT NULL,
  montant       DECIMAL(10, 2) NOT NULL,
  date_paiement DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  mode_paiement ENUM('especes','carte','mobile_money','virement') NOT NULL,
  statut        ENUM('en_attente','confirme','echoue','rembourse') NOT NULL DEFAULT 'en_attente',
  CONSTRAINT fk_paiement_client FOREIGN KEY (id_client)
    REFERENCES clients(id_client) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE IF NOT EXISTS reservations (
  id_reservation   INT AUTO_INCREMENT PRIMARY KEY,
  id_client        INT NOT NULL,
  id_place         INT NOT NULL,
  id_trajet        INT NOT NULL,
  id_paiement      INT NULL,
  date_reservation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  statut           ENUM('en_attente','confirmee','annulee') NOT NULL DEFAULT 'en_attente',
  CONSTRAINT fk_resa_client   FOREIGN KEY (id_client) REFERENCES clients(id_client),
  CONSTRAINT fk_resa_place    FOREIGN KEY (id_place) REFERENCES places(id_place),
  CONSTRAINT fk_resa_trajet   FOREIGN KEY (id_trajet) REFERENCES trajets(id_trajet),
  CONSTRAINT fk_resa_paiement FOREIGN KEY (id_paiement) REFERENCES paiements(id_paiement)
    ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT uq_place_trajet_active UNIQUE (id_place, id_trajet)
);
