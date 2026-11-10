-- Le mart doit correspondre exactement aux observations de l’intermediate.
with expected as (
    select
        observation_year,
        genus,
        count(*) as observation_count
    from {{ ref('int_gbif__observations_annuelles') }}
    group by observation_year, genus
),

actual as (
    select
        observation_year,
        genus,
        observation_count
    from {{ ref('mart_observations_annuelles') }}
),

missing_or_incorrect as (
    select * from expected
    except all
    select * from actual
),

unexpected as (
    select * from actual
    except all
    select * from expected
)

select * from missing_or_incorrect
union all
select * from unexpected
