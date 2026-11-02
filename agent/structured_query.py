"""Décrit et valide une demande structurée de comptage des observations."""

from pydantic import BaseModel, Field, field_validator

class ObservationQuery(BaseModel):
    """Genre taxonomique et année : borne supérieure actuellement figée à 2026."""
    genus: str = Field(min_length=1)
    year : int = Field(ge=1800, le=2026)

    @field_validator("genus", mode="before")
    @classmethod
    def nettoyer_genus(cls, value):
        """Retire les espaces avant de vérifier que le genre n’est pas vide."""
        if isinstance(value, str):
            return value.strip()
        return value


# Exemple construit à l’import ; il ne déclenche aucun appel externe.
query = ObservationQuery(
    genus="Panthera",
      year=2026)


