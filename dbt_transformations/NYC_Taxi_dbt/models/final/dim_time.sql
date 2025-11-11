with times as (
    select distinct time(tpep_pickup_datetime) as trip_time
    from {{ ref('yellow_taxi_trips_stg') }}
    union distinct
    select distinct time(tpep_dropoff_datetime) as trip_time
    from {{ ref('yellow_taxi_trips_stg') }}
)

select
    trip_time,
    row_number() over (order by time) as time_key,
    extract(hour from time) as hour,
    extract(minute from time) as minute,
    extract(second from time) as second
from times
