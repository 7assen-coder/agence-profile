-- ============================================================
--  BASE DE DONNÉES : Plateforme de Réservation de Transport
--  Basée sur le MCD fourni (alternatives Alt1, Alt2, Alt3)
-- ============================================================

CREATE DATABASE IF NOT EXISTS transport_reservation
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE transport_reservation;

-- ============================================================
-- 1. TABLE : agences
-- ============================================================
CREATE TABLE agences (
    id_agence   INT AUTO_INCREMENT PRIMARY KEY,
    nom         VARCHAR(100) NOT NULL,
    telephone   VARCHAR(20),
    email       VARCHAR(100),
    adresse     VARCHAR(200)
);

-- ============================================================
-- 2. TABLE : villes
-- ============================================================
CREATE TABLE villes (
    id_ville    INT AUTO_INCREMENT PRIMARY KEY,
    nom         VARCHAR(100) NOT NULL,
    region      VARCHAR(100)
);

-- ============================================================
-- 3. TABLE : bus
--    Alt 2 : Bus appartient à une Agence
--             Les places sont liées au Bus (physique/fixe)
-- ============================================================
CREATE TABLE bus (
    id_bus          INT AUTO_INCREMENT PRIMARY KEY,
    id_agence       INT NOT NULL,
    immatriculation VARCHAR(20) NOT NULL UNIQUE,
    capacite        INT NOT NULL DEFAULT 12,
    CONSTRAINT fk_bus_agence FOREIGN KEY (id_agence)
        REFERENCES agences(id_agence)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================================
-- 4. TABLE : places
--    Alt 2 : Place liée au Bus (pas au trajet)
--    12 places numérotées (1 à 12) par bus
-- ============================================================
CREATE TABLE places (
    id_place        INT AUTO_INCREMENT PRIMARY KEY,
    id_bus          INT NOT NULL,
    numero_place    TINYINT NOT NULL CHECK (numero_place BETWEEN 1 AND 12),
    CONSTRAINT fk_place_bus FOREIGN KEY (id_bus)
        REFERENCES bus(id_bus)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT uq_place_bus UNIQUE (id_bus, numero_place)
);

-- ============================================================
-- 5. TABLE : trajets
--    Alt 1 : Ville utilisée 2x → id_ville_depart + id_ville_arrivee
-- ============================================================
CREATE TABLE trajets (
    id_trajet           INT AUTO_INCREMENT PRIMARY KEY,
    id_agence           INT NOT NULL,
    id_bus              INT NOT NULL,
    id_ville_depart     INT NOT NULL,
    id_ville_arrivee    INT NOT NULL,
    date_trajet         DATE NOT NULL,
    periode             ENUM('matin', 'apres-midi') NOT NULL,
    heure_depart        TIME,
    heure_arrivee       TIME,
    prix                DECIMAL(10, 2) NOT NULL,
    CONSTRAINT fk_trajet_agence  FOREIGN KEY (id_agence)
        REFERENCES agences(id_agence)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_trajet_bus     FOREIGN KEY (id_bus)
        REFERENCES bus(id_bus)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_trajet_depart  FOREIGN KEY (id_ville_depart)
        REFERENCES villes(id_ville)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_trajet_arrivee FOREIGN KEY (id_ville_arrivee)
        REFERENCES villes(id_ville)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================================
-- 6. TABLE : clients
-- ============================================================
CREATE TABLE clients (
    id_client   INT AUTO_INCREMENT PRIMARY KEY,
    nom         VARCHAR(100) NOT NULL,
    prenom      VARCHAR(100) NOT NULL,
    telephone   VARCHAR(20),
    email       VARCHAR(100) UNIQUE,
    cin         VARCHAR(20) UNIQUE          -- Carte d'identité nationale
);

-- ============================================================
-- 7. TABLE : paiements
--    Alt 3 : Paiement lié au Client en amont,
--             il génère ensuite la Réservation
-- ============================================================
CREATE TABLE paiements (
    id_paiement     INT AUTO_INCREMENT PRIMARY KEY,
    id_client       INT NOT NULL,
    montant         DECIMAL(10, 2) NOT NULL,
    date_paiement   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    mode_paiement   ENUM('especes', 'carte', 'mobile_money', 'virement') NOT NULL,
    statut          ENUM('en_attente', 'confirme', 'echoue', 'rembourse')
                    NOT NULL DEFAULT 'en_attente',
    CONSTRAINT fk_paiement_client FOREIGN KEY (id_client)
        REFERENCES clients(id_client)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);

-- ============================================================
-- 8. TABLE : reservations
--    Liée à : Client, Place, Trajet, Paiement
--    Contrainte : une place = une seule réservation active par trajet
-- ============================================================
CREATE TABLE reservations (
    id_reservation  INT AUTO_INCREMENT PRIMARY KEY,
    id_client       INT NOT NULL,
    id_place        INT NOT NULL,
    id_trajet       INT NOT NULL,
    id_paiement     INT,                    -- NULL avant confirmation
    date_reservation DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    statut          ENUM('en_attente', 'confirmee', 'annulee')
                    NOT NULL DEFAULT 'en_attente',
    CONSTRAINT fk_resa_client   FOREIGN KEY (id_client)
        REFERENCES clients(id_client)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_resa_place    FOREIGN KEY (id_place)
        REFERENCES places(id_place)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_resa_trajet   FOREIGN KEY (id_trajet)
        REFERENCES trajets(id_trajet)
        ON DELETE RESTRICT
        ON UPDATE CASCADE,
    CONSTRAINT fk_resa_paiement FOREIGN KEY (id_paiement)
        REFERENCES paiements(id_paiement)
        ON DELETE SET NULL
        ON UPDATE CASCADE,
    -- Une place ne peut avoir qu'une seule réservation active par trajet
    CONSTRAINT uq_place_trajet_active
        UNIQUE (id_place, id_trajet)
);

