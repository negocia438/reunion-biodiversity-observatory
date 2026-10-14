INSERT INTO raw.source_files (
    source_name,
    gbif_id,
    file_name,
    checksum_sha256,
    file_size_bytes,
    source_created_at,
    file_modified_at,
    source_url
)
VALUES (
    'GBIF',
    '0021471-260928105237408',
    '0021471-260928105237408.zip',
    'baabbdd042aeffa0872d3e968ce411677016e233fa3c68292c15e898e6568926',
    253248972,
    '2026-10-12T12:24:45Z',
    '2026-10-12 18:47:21.696041336 +0200',
    'https://api.gbif.org/v1/occurrence/download/request/0021471-260928105237408.zip'
);
