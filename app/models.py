from .database import *

CAPACITES_VALIDES = {15, 32, 60}


def generer_places(bus_id: int, capacite: int) -> dict:
    """
    Génère les places numérotées de 1 à `capacite` pour le bus donné.

    Retourne un dict avec le résultat de l'opération.
    Lève ValueError si la capacité n'est pas autorisée.
    Lève RuntimeError si les places existent déjà pour ce bus.
    """
    if capacite not in CAPACITES_VALIDES:
        raise ValueError(
            f"Capacité {capacite} invalide. Valeurs acceptées : {sorted(CAPACITES_VALIDES)}"
        )

    db = init_db()
    cur = db.cursor()

    cur.execute("SELECT COUNT(*) FROM place WHERE bus_id = ?", (bus_id,))
    (existantes,) = cur.fetchone()
    if existantes > 0:
        raise RuntimeError(
            f"Les places du bus {bus_id} ont déjà été générées ({existantes} places en base)."
        )

    places = [(bus_id, num_place) for num_place in range(1, capacite + 1)]
    cur.executemany(
        "INSERT INTO place (bus_id, numero_place) VALUES (?, ?)",
        places,
    )
    db.commit()
    cur.close()

    return {
        "bus_id": bus_id,
        "capacite": capacite,
        "places_generees": capacite,
        "message": f"{capacite} places générées avec succès pour le bus {bus_id}.",
    }


def get_places_par_bus(bus_id: int) -> list[dict]:
    """
    Retourne toutes les places d'un bus avec leur statut.
    Appelé par l'équipe affichage.
    """
    db = init_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT p.id_place, p.numero_place, p.bus_id
        FROM place p
        WHERE p.bus_id = ?
        ORDER BY p.numero_place ASC
        """,
        (bus_id,),
    )
    rows = cur.fetchall()
    cur.close()

    return [
        {
            "id_place": row[0],
            "numero_place": row[1],
            "bus_id": row[2],
        }
        for row in rows
    ]


def supprimer_places(bus_id: int) -> dict:
    """
    Supprime toutes les places d'un bus (utile en cas de reconfiguration).
    """
    db = init_db()
    cur = db.cursor()
    cur.execute("DELETE FROM place WHERE bus_id = ?", (bus_id,))
    supprimees = cur.rowcount
    db.commit()
    cur.close()

    return {
        "bus_id": bus_id,
        "places_supprimees": supprimees,
        "message": f"{supprimees} place(s) supprimée(s) pour le bus {bus_id}.",
    }
