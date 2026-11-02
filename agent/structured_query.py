"""Décrit et valide une demande structurée de comptage des observations."""

from pydantic import BaseModel, Field

class ObservationQuery(BaseModel):
    """Genre taxonomique et année : borne supérieure actuellement figée à 2026."""
    genus : str
    year : int = Field(ge=1800, le=2026)


# Exemple construit à l’import ; il ne déclenche aucun appel externe.
query = ObservationQuery(
    genus="Panthera",
      year=2026)


