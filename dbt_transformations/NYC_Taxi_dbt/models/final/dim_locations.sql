with locations as (
    select distinct pulocationid as location_id
    from {{ ref('yellow_taxi_trips_stg') }}
    union distinct
    select distinct dolocationid as location_id
    from {{ ref('yellow_taxi_trips_stg') }}
)

select
    location_id,
    row_number() over (order by location_id) as location_key
from locations
