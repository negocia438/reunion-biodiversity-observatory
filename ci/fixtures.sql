CREATE SCHEMA raw;

CREATE TABLE raw.gbif_occurrences_full (
    "gbifID" TEXT,
    "year" TEXT,
    "genus" TEXT,
    "species" TEXT,
    "scientificName" TEXT,
    "countryCode" TEXT,
    "basisOfRecord" TEXT,
    "occurrenceStatus" TEXT
);

INSERT INTO raw.gbif_occurrences_full (
    "gbifID",
    "year",
    "genus",
    "countryCode"
)
VALUES
    ('1', '2024', 'Phelsuma', 'RE'),
    ('2', ' 2024 ', ' Phelsuma ', 'RE'),
    ('3', '2025', '', 'RE'),
    ('4', '', 'Phelsuma', 'RE'),
    ('5', 'inconnu', 'Phelsuma', 'RE'),
    (
        '6',
        (EXTRACT(YEAR FROM CURRENT_DATE)::INTEGER + 1)::TEXT,
        'Phelsuma',
        'RE'
    );
