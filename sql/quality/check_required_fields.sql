SELECT COUNT(*) AS invalid_observations
FROM raw.gbif_occurrences
WHERE gbif_key IS NULL
   OR species IS NULL
   OR scientific_name IS NULL
   OR event_date IS NULL
   OR latitude IS NULL
   OR longitude IS NULL;
