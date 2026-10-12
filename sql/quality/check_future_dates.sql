SELECT COUNT(*) AS future_observations
FROM raw.gbif_occurrences
WHERE event_date > NOW();
