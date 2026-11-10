-- Les chiffres fixes de ce test ne concernent que les données fictives.
{{ config(enabled=target.name == 'ci') }}

select 'staging incorrect' as anomaly
where
    (select count(*) from {{ ref('stg_gbif__occurrences') }}) <> 6
    or (
        select count(*)
        from {{ ref('stg_gbif__occurrences') }}
        where observation_year is null
    ) <> 2

union all

select 'intermediate incorrect' as anomaly
where
    (select count(*) from {{ ref('int_gbif__observations_annuelles') }}) <> 3

union all

select 'mart incorrect' as anomaly
where
    (select count(*) from {{ ref('mart_observations_annuelles') }}) <> 2
    or (
        select coalesce(sum(observation_count), 0)
        from {{ ref('mart_observations_annuelles') }}
    ) <> 3
    or (
        select count(*)
        from {{ ref('mart_observations_annuelles') }}
        where observation_year = 2024
          and genus = 'Phelsuma'
          and observation_count = 2
    ) <> 1
    or (
        select count(*)
        from {{ ref('mart_observations_annuelles') }}
        where observation_year = 2025
          and genus is null
          and observation_count = 1
    ) <> 1
