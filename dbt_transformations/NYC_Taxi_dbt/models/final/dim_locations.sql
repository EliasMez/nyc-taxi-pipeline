with locations as (
    select distinct
        pulocationid as location_id
    from {{ ref('yellow_taxi_trips_stg') }}
    union
    select distinct
        dolocationid as location_id
    from {{ ref('yellow_taxi_trips_stg') }}
)
select
    row_number() over (order by location_id) as location_key,
    location_id
from locations