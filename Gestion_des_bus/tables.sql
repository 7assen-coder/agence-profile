-- ============================================================
--  GROUPE 8 — Table bus uniquement
--  Matricules : 251081 – 251048 – 251083
-- ============================================================

USE transport_db;

-- ⚠️ Prérequis : tables agences et trajets déjà créées

CREATE TABLE IF NOT EXISTS bus (
    id              INT         AUTO_INCREMENT PRIMARY KEY,
    immatriculation VARCHAR(20) NOT NULL UNIQUE,
    capacite        INT         NOT NULL DEFAULT 12,  -- toujours 12, jamais modifiable
    agence_id       INT         NOT NULL,
    trajet_id       INT,                              -- NULL = bus non assigné
    created_at      DATETIME    NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_bus_agence
        FOREIGN KEY (agence_id)
        REFERENCES agences(id)
        ON DELETE RESTRICT,

    CONSTRAINT fk_bus_trajet
        FOREIGN KEY (trajet_id)
        REFERENCES trajets(id)
        ON DELETE SET NULL,

    CONSTRAINT chk_capacite CHECK (capacite = 12)    -- bloqué à 12 strictement
);
