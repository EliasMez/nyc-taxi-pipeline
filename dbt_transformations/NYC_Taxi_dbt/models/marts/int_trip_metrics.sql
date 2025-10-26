with base as (
    select * from {{ ref('yellow_taxi_trips_stg') }}
)
select
    *,
    datediff('minute', TO_TIMESTAMP(tpep_pickup_datetime), TO_TIMESTAMP(tpep_dropoff_datetime)) as trip_duration_minutes,
    extract(hour from TO_TIMESTAMP(tpep_pickup_datetime)) as pickup_hour,
    extract(day from TO_TIMESTAMP(tpep_pickup_datetime)) as pickup_day,
    extract(month from TO_TIMESTAMP(tpep_pickup_datetime)) as pickup_month,
    case when datediff('second', TO_TIMESTAMP(tpep_pickup_datetime), TO_TIMESTAMP(tpep_dropoff_datetime)) > 0
        then trip_distance * 3600.0 / datediff('second', TO_TIMESTAMP(tpep_pickup_datetime), TO_TIMESTAMP(tpep_dropoff_datetime))
        else null end as avg_speed_mph,
    case when fare_amount > 0 then tip_amount / fare_amount else null end as tip_pct
from base