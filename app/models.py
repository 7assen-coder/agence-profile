from .database import *

CAPACITES_VALIDES = {12, 32, 60}


def generer_places(id_bus: int, capacite: int) -> dict:
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

    cur.execute("SELECT COUNT(*) FROM places WHERE id_bus = ?", (id_bus,))
    (existantes,) = cur.fetchone()
    if existantes > 0:
        raise RuntimeError(
            f"Les places du bus {id_bus} ont déjà été générées ({existantes} places en base)."
        )

    places = [(id_bus, num_place) for num_place in range(1, capacite + 1)]
    cur.executemany(
        "INSERT INTO places (id_bus, numero_place) VALUES (?, ?)",
        places,
    )
    db.commit()
    cur.close()

    return {
        "id_bus": id_bus,
        "capacite": capacite,
        "places_generees": capacite,
        "message": f"{capacite} places générées avec succès pour le bus {id_bus}.",
    }


def get_places_par_bus(id_bus: int) -> list[dict]:
    """
    Retourne toutes les places d'un bus avec leur statut.
    Appelé par l'équipe affichage.
    """
    db = init_db()
    cur = db.cursor()
    cur.execute(
        """
        SELECT p.id_place, p.numero_place, p.id_bus
        FROM places p
        WHERE p.id_bus = ?
        ORDER BY p.numero_place ASC
        """,
        (id_bus,),
    )
    rows = cur.fetchall()
    cur.close()

    return [
        {
            "id_place": row[0],
            "numero_place": row[1],
            "id_bus": row[2],
        }
        for row in rows
    ]


def supprimer_places(id_bus: int) -> dict:
    """
    Supprime toutes les places d'un bus (utile en cas de reconfiguration).
    """
    db = init_db()
    cur = db.cursor()
    cur.execute("DELETE FROM places WHERE id_bus = ?", (id_bus,))
    supprimees = cur.rowcount
    db.commit()
    cur.close()

    return {
        "id_bus": id_bus,
        "places_supprimees": supprimees,
        "message": f"{supprimees} place(s) supprimée(s) pour le bus {id_bus}.",
    }
