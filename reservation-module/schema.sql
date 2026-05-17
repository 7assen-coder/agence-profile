-- Module : Réservation des places
-- À ajouter au schéma commun du projet SaaS Trajets

USE trajets_saas;

CREATE TABLE IF NOT EXISTS reservations (
  id               INT AUTO_INCREMENT PRIMARY KEY,
  trajet_id        INT          NOT NULL,
  client_nom       VARCHAR(120) NOT NULL,
  client_email     VARCHAR(120) NOT NULL,
  client_telephone VARCHAR(30)  NULL,
  numero_place     INT          NOT NULL CHECK (numero_place BETWEEN 1 AND 12),
  statut           ENUM('en_attente', 'confirmee', 'annulee') NOT NULL DEFAULT 'en_attente',
  date_expiration  DATETIME     NULL,       -- blocage temporaire (15 min)
  date_creation    DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_maj         DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

  INDEX idx_reservation_trajet  (trajet_id),
  INDEX idx_reservation_statut  (statut),
  INDEX idx_reservation_email   (client_email),
  UNIQUE KEY uq_place_trajet    (trajet_id, numero_place, statut)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
