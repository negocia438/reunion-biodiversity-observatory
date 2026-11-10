-- Une ligne par année et par genre, y compris les genres absents.
select
    observation_year,
    genus,
    count(*) as observation_count
from {{ ref('int_gbif__observations_annuelles') }}
group by
    observation_year,
    genus
