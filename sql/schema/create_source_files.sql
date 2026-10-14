CREATE TABLE raw.source_files (
    source_id BIGSERIAL PRIMARY KEY,
    source_name TEXT NOT NULL,
    gbif_id TEXT NOT NULL UNIQUE,
    file_name TEXT NOT NULL,
    checksum_sha256 TEXT NOT NULL UNIQUE,
    file_size_bytes BIGINT NOT NULL,
    source_created_at TIMESTAMPTZ NOT NULL,
    file_modified_at TIMESTAMPTZ,
    source_url TEXT NOT NULL
);
