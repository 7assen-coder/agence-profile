## Module : Validation des données

Ce module vérifie les données envoyées par les formulaires avant leur insertion dans la base MySQL.

Fichiers ajoutés :
- `app/utils/validators.py` : fonctions génériques de validation.
- `app/schemas/validation_schemas.py` : règles de validation métier.
- `tests/test_validation.py` : tests unitaires des règles de validation.

Règles couvertes :
- validation des agences
- validation des clients
- validation des villes
- validation des trajets
- validation des bus et des places
- validation des réservations
- validation des paiements