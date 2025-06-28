# Fichier: constants.py

SHEETS_CONFIG = {
    "disponibilites": "https://docs.google.com/spreadsheets/d/113KAFUl9E4ceFqm-gIfQ-zhigYGnOGPh/export?format=xlsx",
    "arbitres": "https://docs.google.com/spreadsheets/d/1UUZBFPMCkVGzVKeTP_D44ZpGwTHlu0Q0/export?format=xlsx",
    "rencontres": "https://docs.google.com/spreadsheets/d/1cM3QiYhiu22sKSgYKvpahvNWJqlxSk-e/export?format=xlsx"  # À compléter
}

# Niveaux de compétition (exemple)
NIVEAU_COMPETITIONS = {
    "LIGUE 1": (5, 6),
    "LIGUE 2": (4, 5),
    "NATIONAL": (3, 4)
}

# Mapping des catégories d'arbitres à un niveau numérique
CATEGORIE_NIVEAU = {
    "F1": 6, "F2": 5, "F3": 4, "F4": 3,
    "J1": 3, "J2": 2, "J3": 1
}
