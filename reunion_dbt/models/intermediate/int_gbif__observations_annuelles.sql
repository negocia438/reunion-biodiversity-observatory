-- Observations exploitables pour une analyse annuelle.
-- Les lignes RAW restent intactes.
select
    gbif_id,
    observation_year,
    genus,
    species,
    country_code,
    basis_of_record,
    occurrence_status
from {{ ref('stg_gbif__occurrences') }}
where observation_year between 1
    and extract(year from current_date)
