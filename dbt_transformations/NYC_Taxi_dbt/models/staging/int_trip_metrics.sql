with base as (
    select * from {{ ref('yellow_taxi_trips_stg') }}
)

select
    *,
    datediff('minute', to_timestamp(tpep_pickup_datetime), to_timestamp(tpep_dropoff_datetime)) as trip_duration_minutes,
    extract(hour from to_timestamp(tpep_pickup_datetime)) as pickup_hour,
    extract(day from to_timestamp(tpep_pickup_datetime)) as pickup_day,
    extract(month from to_timestamp(tpep_pickup_datetime)) as pickup_month,
    date(to_timestamp(tpep_pickup_datetime)) as pickup_date,
    case
        when datediff('second', to_timestamp(tpep_pickup_datetime), to_timestamp(tpep_dropoff_datetime)) > 0
            then (trip_distance * 3600.0 / datediff('second', to_timestamp(tpep_pickup_datetime), to_timestamp(tpep_dropoff_datetime)))::NUMBER(10,2)
    end as avg_speed_mph,
    case when fare_amount > 0 then (tip_amount / fare_amount)::NUMBER(10,2) end as tip_pct
from base