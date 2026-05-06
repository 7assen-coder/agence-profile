from .database import get_db

CAPACITES_VALIDES = {12, 32, 60}


def _cursor(dictionary=True):
    return get_db().cursor(dictionary=dictionary)


# ── Helpers requêtes bus ────────────────────────────────────────────────────

def get_bus(id_bus: int) -> dict | None:
    cur = _cursor()
    cur.execute(
        """
        SELECT b.id_bus, b.immatriculation, b.capacite,
               a.nom AS nom_agence
        FROM bus b
        JOIN agences a ON a.id_agence = b.id_agence
        WHERE b.id_bus = %s
        """,
        (id_bus,),
    )
    row = cur.fetchone()
    cur.close()
    return row


def get_all_bus() -> list[dict]:
    cur = _cursor()
    cur.execute(
        """
        SELECT b.id_bus, b.immatriculation, b.capacite,
               a.nom AS nom_agence,
               COUNT(p.id_place) AS nb_places_generees
        FROM bus b
        JOIN agences a ON a.id_agence = b.id_agence
        LEFT JOIN places p ON p.id_bus = b.id_bus
        GROUP BY b.id_bus
        ORDER BY b.id_bus
        """
    )
    rows = cur.fetchall()
    cur.close()
    return rows


# ── Génération des places ───────────────────────────────────────────────────

def generer_places(id_bus: int, capacite: int | None = None) -> dict:
    """
    Génère les places numérotées 1..capacite pour le bus donné.
    Si capacite est None, utilise la capacite stockée dans la table bus.
    """
    bus = get_bus(id_bus)
    if not bus:
        raise ValueError(f"Bus {id_bus} introuvable en base.")

    cap = capacite if capacite is not None else bus["capacite"]

    if cap not in CAPACITES_VALIDES:
        raise ValueError(
            f"Capacité {cap} invalide. Valeurs acceptées : {sorted(CAPACITES_VALIDES)}"
        )

    db = get_db()
    cur = db.cursor(dictionary=True)

    cur.execute("SELECT COUNT(*) AS n FROM places WHERE id_bus = %s", (id_bus,))
    if cur.fetchone()["n"] > 0:
        cur.close()
        raise RuntimeError(
            f"Les places du bus {id_bus} ont déjà été générées."
        )

    cur.executemany(
        "INSERT INTO places (id_bus, numero_place) VALUES (%s, %s)",
        [(id_bus, num) for num in range(1, cap + 1)],
    )
    db.commit()
    cur.close()

    return {
        "id_bus": id_bus,
        "immatriculation": bus["immatriculation"],
        "capacite": cap,
        "places_generees": cap,
        "message": f"{cap} places générées avec succès pour le bus {id_bus}.",
    }


# ── Lecture des places ──────────────────────────────────────────────────────

def get_places_par_bus(id_bus: int) -> list[dict]:
    """
    Retourne les places avec leur statut de réservation
    sur le trajet le plus récent du bus.
    """
    cur = _cursor()
    cur.execute(
        """
        SELECT
            p.id_place,
            p.numero_place,
            p.id_bus,
            CASE
                WHEN r.id_reservation IS NOT NULL
                     AND r.statut IN ('en_attente', 'confirmee')
                THEN r.statut
                ELSE 'libre'
            END AS statut_place,
            r.id_trajet
        FROM places p
        LEFT JOIN reservations r
            ON r.id_place = p.id_place
            AND r.statut IN ('en_attente', 'confirmee')
        WHERE p.id_bus = %s
        ORDER BY p.numero_place ASC
        """,
        (id_bus,),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


def get_places_par_trajet(id_bus: int, trajet_id: int) -> list[dict]:
    """
    Retourne les places avec leur statut pour un trajet précis.
    """
    cur = _cursor()
    cur.execute(
        """
        SELECT
            p.id_place,
            p.numero_place,
            p.id_bus,
            CASE
                WHEN r.id_reservation IS NOT NULL THEN r.statut
                ELSE 'libre'
            END AS statut_place
        FROM places p
        LEFT JOIN reservations r
            ON r.id_place = p.id_place
            AND r.id_trajet = %s
            AND r.statut IN ('en_attente', 'confirmee')
        WHERE p.id_bus = %s
        ORDER BY p.numero_place ASC
        """,
        (trajet_id, id_bus),
    )
    rows = cur.fetchall()
    cur.close()
    return rows


# ── Suppression des places ──────────────────────────────────────────────────

def supprimer_places(id_bus: int) -> dict:
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM places WHERE id_bus = %s", (id_bus,))
    supprimees = cur.rowcount
    db.commit()
    cur.close()
    return {
        "id_bus": id_bus,
        "places_supprimees": supprimees,
        "message": f"{supprimees} place(s) supprimée(s) pour le bus {id_bus}.",
    }


# ── Stats pour le dashboard ─────────────────────────────────────────────────

def get_stats() -> dict:
    cur = _cursor()

    cur.execute("SELECT COUNT(*) AS n FROM bus")
    nb_bus = cur.fetchone()["n"]

    cur.execute("SELECT COUNT(*) AS n FROM places")
    nb_places = cur.fetchone()["n"]

    cur.execute(
        "SELECT COUNT(*) AS n FROM bus b "
        "WHERE (SELECT COUNT(*) FROM places p WHERE p.id_bus = b.id_bus) = 0"
    )
    bus_sans_places = cur.fetchone()["n"]

    cur.execute(
        "SELECT COUNT(*) AS n FROM reservations "
        "WHERE statut IN ('en_attente','confirmee')"
    )
    nb_reservations = cur.fetchone()["n"]

    cur.close()
    return {
        "nb_bus": nb_bus,
        "nb_places": nb_places,
        "bus_sans_places": bus_sans_places,
        "nb_reservations": nb_reservations,
    }
