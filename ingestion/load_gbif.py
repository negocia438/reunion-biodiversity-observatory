import os
import json

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

            values = {
                "gbif_key": obs.get("key"),
                "occurrence_id": obs.get("occurrenceID"),
                "scientific_name": obs.get("scientificName"),
                "species": obs.get("species"),
                "genus": obs.get("genus"),
                "family": obs.get("family"),
                "class_name": obs.get("class"),
                "taxon_key": obs.get("taxonKey"),
                "iucn_category": obs.get("iucnRedListCategory"),
                "event_date": obs.get("eventDate"),
                "latitude": obs.get("decimalLatitude"),
                "longitude": obs.get("decimalLongitude"),
                "state_province": obs.get("stateProvince"),
                "country_code": obs.get("countryCode"),
                "basis_of_record": obs.get("basisOfRecord"),
                "occurrence_status": obs.get("occurrenceStatus"),
                "dataset_name": obs.get("datasetName"),
                "recorded_by": obs.get("recordedBy"),
                "license": obs.get("license"),
                "issues": json.dumps(obs.get("issues")),
                "source_modified_at": obs.get("modified"),
                "gbif_interpreted_at": obs.get("lastInterpreted"),
                "source_reference": obs.get("references"),
                "raw_payload": json.dumps(obs)
            }

            cur.execute(
                """
                INSERT INTO raw.gbif_occurrences (
                    gbif_key,
                    occurrence_id,
                    scientific_name,
                    species,
                    genus,
                    family,
                    class_name,
                    taxon_key,
                    iucn_category,
                    event_date,
                    latitude,
                    longitude,
                    state_province,
                    country_code,
                    basis_of_record,
                    occurrence_status,
                    dataset_name,
                    recorded_by,
                    license,
                    issues,
                    source_modified_at,
                    gbif_interpreted_at,
                    source_reference,
                    raw_payload
                )
                VALUES (
                    %(gbif_key)s,
                    %(occurrence_id)s,
                    %(scientific_name)s,
                    %(species)s,
                    %(genus)s,
                    %(family)s,
                    %(class_name)s,
                    %(taxon_key)s,
                    %(iucn_category)s,
                    %(event_date)s,
                    %(latitude)s,
                    %(longitude)s,
                    %(state_province)s,
                    %(country_code)s,
                    %(basis_of_record)s,
                    %(occurrence_status)s,
                    %(dataset_name)s,
                    %(recorded_by)s,
                    %(license)s,
                    %(issues)s,
                    %(source_modified_at)s,
                    %(gbif_interpreted_at)s,
                    %(source_reference)s,
                    %(raw_payload)s
                )
                ON CONFLICT (gbif_key) DO NOTHING
                """,
                values
            )

print("Import GBIF terminé")