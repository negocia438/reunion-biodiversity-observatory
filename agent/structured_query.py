from pydantic import BaseModel, Field

class ObservationQuery(BaseModel):
    genus : str
    year : int = Field(ge=1800, le=2026)


query = ObservationQuery(
    genus="Panthera",
      year=2026)


