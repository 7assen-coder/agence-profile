-- Schéma commun du projet SaaS Trajets
-- Ce fichier ne contient QUE la table gérée par le module "Gestion Profil Agence".
-- Les autres groupes ajouteront leurs tables (trajets, reservations, paiements, etc.).

CREATE DATABASE IF NOT EXISTS trajets_saas
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_unicode_ci;

USE trajets_saas;

CREATE TABLE IF NOT EXISTS agences (
  id             INT AUTO_INCREMENT PRIMARY KEY,
  nom            VARCHAR(120)  NOT NULL,
  email          VARCHAR(120)  NOT NULL UNIQUE,
  password_hash  VARCHAR(255)  NOT NULL,
  telephone      VARCHAR(30)   NULL,
  adresse        VARCHAR(255)  NULL,
  ville          VARCHAR(80)   NULL,
  description    TEXT          NULL,
  logo           VARCHAR(255)  NULL,
  statut         ENUM('active','suspendue','en_attente') NOT NULL DEFAULT 'en_attente',
  role           ENUM('agence','admin') NOT NULL DEFAULT 'agence',
  date_creation  DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_maj       DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_agence_statut (statut),
  INDEX idx_agence_ville (ville)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
