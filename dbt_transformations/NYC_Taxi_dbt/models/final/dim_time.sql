with times as (
    select distinct
        time(tpep_pickup_datetime) as time
    from {{ ref('yellow_taxi_trips_stg') }}
    union
    select distinct
        time(tpep_dropoff_datetime) as time
    from {{ ref('yellow_taxi_trips_stg') }}
)
select
    row_number() over (order by time) as time_key,
    time,
    extract(hour from time) as hour,
    extract(minute from time) as minute,
    extract(second from time) as second,
from times