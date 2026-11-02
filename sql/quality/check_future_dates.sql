-- Compte les dates futures dans la table issue de l’import API ; ne modifie aucune ligne.
SELECT COUNT(*) AS future_observations
FROM raw.gbif_occurrences
WHERE event_date > NOW();
