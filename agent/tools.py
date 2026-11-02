"""Outils métier du prototype : les résultats sont fixes, sans requête PostgreSQL."""

def get_observation_count(genus: str, year: int) -> int:
    """Retourne le nombre d'observations GBIF pour un genre et une année."""
    # Valeur de démonstration : genus et year ne sont pas encore utilisés.
    return 127


def get_data_freshness() -> str:
    """Retourne la date de dernière mise à jour des données GBIF."""
    # Date illustrative, sans lecture de la base ni des métadonnées GBIF.
    return "2026-10-20"