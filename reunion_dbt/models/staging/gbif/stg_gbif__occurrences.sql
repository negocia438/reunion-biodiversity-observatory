-- Une ligne par ligne RAW : aucun filtre ni dédoublonnage.
with cleaned as (
    select
        nullif(trim("gbifID"), '') as gbif_id,
        nullif(trim("year"), '') as observation_year_raw,
        nullif(trim("genus"), '') as genus,
        nullif(trim("species"), '') as species,
        nullif(trim("scientificName"), '') as scientific_name,
        nullif(trim("countryCode"), '') as country_code,
        nullif(trim("basisOfRecord"), '') as basis_of_record,
        nullif(trim("occurrenceStatus"), '') as occurrence_status
    from {{ source('gbif', 'gbif_occurrences_full') }}
)

select
    gbif_id,
    case
        when observation_year_raw ~ '^[0-9]{1,4}$'
            then observation_year_raw::integer
        else null
    end as observation_year,
    observation_year_raw,
    genus,
    species,
    scientific_name,
    country_code,
    basis_of_record,
    occurrence_status
from cleaned
