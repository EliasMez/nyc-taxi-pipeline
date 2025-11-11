with dates as (
    select distinct date(tpep_pickup_datetime) as trip_date
    from {{ ref('yellow_taxi_trips_stg') }}
    union distinct
    select distinct date(tpep_dropoff_datetime) as trip_date
    from {{ ref('yellow_taxi_trips_stg') }}
)

select
    trip_date,
    row_number() over (order by trip_date) as date_key,
    extract(year from trip_date) as year,
    extract(month from trip_date) as month,
    extract(day from trip_date) as day,
    extract(quarter from trip_date) as quarter,
    extract(dayofweek from trip_date) as day_of_week
from dates
