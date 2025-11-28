with times as (
    select distinct time(tpep_pickup_datetime) as trip_time
    from {{ ref('yellow_taxi_trips_stg') }}
    union distinct
    select distinct time(tpep_dropoff_datetime) as trip_time
    from {{ ref('yellow_taxi_trips_stg') }}
)

select
    to_char(trip_time, 'HH24MISS')::integer as time_key,
    trip_time,
    extract(hour from trip_time) as hour,
    extract(minute from trip_time) as minute,
    extract(second from trip_time) as second
from times
