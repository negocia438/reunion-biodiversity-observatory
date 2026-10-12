SELECT COUNT(*) AS invalid_geographic_observations
FROM raw.gbif_occurrences
WHERE latitude < -21.40
   OR latitude > -20.80
   OR longitude < 55.20
   OR longitude > 55.90;
