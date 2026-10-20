from google import genai
from structured_query import ObservationQuery
from tools import get_observation_count

client = genai.Client()

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Combien d'observations de Phelsuma avons-nous en 2024 ?",
    config={
        "response_mime_type": "application/json",
        "response_schema": ObservationQuery,
    }
)

query = response.parsed

result = get_observation_count(
    genus=query.genus,
    year=query.year
)