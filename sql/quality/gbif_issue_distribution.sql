SELECT
    issue,
    COUNT(*) AS nb_occurrences
FROM raw.gbif_occurrences
CROSS JOIN LATERAL jsonb_array_elements_text(issues) AS issue
GROUP BY issue
ORDER BY nb_occurrences DESC;
