"""Démonstration Gemini : extraction JSON puis appel explicite à un outil simulé.

Ce script contacte Gemini dès son exécution ; ce n’est pas un test unitaire."""

from google import genai
from structured_query import ObservationQuery
from tools import get_observation_count

# Le SDK lit les identifiants dans l’environnement ; aucun .env n’est chargé ici.
client = genai.Client()

# Le schéma Pydantic contraint la structure JSON attendue.
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Combien d'observations de Phelsuma avons-nous en 2024 ?",
    config={
        "response_mime_type": "application/json",
        "response_schema": ObservationQuery,
    }
)

# Le SDK expose la réponse interprétée sous forme de modèle ObservationQuery.
query = response.parsed

# Le résultat reste dans la variable result ; ce script ne l’affiche pas.
result = get_observation_count(
    genus=query.genus,
    year=query.year
)