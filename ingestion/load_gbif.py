import os

import psycopg
import requests


url = "https://api.gbif.org/v1/occurrence/search"

params = {
    "country": "RE",
    "limit": 10
}

response = requests.get(url, params=params)
response.raise_for_status()

data = response.json()

password = os.environ["DB_PASSWORD"]

conn = psycopg.connect(
    host="localhost",
    dbname="reunion_biodiversity",
    user="reunion_user",
    password=password
)

with conn:
    with conn.cursor() as cur:
        for obs in data["results"]:
            cur.execute(
                """
                INSERT INTO raw.gbif_occurrences (
                    gbif_key,
                    species,
                    latitude
                )
                VALUES (
                    %(key)s,
                    %(species)s,
                    %(decimalLatitude)s
                )
                ON CONFLICT (gbif_key) DO NOTHING
                """,
                obs
            )

print("Import GBIF terminé")