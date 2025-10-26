with dates as (
    select distinct
        date(tpep_pickup_datetime) as date
    from {{ ref('yellow_taxi_trips_stg') }}
    union
    select distinct
        date(tpep_dropoff_datetime) as date
    from {{ ref('yellow_taxi_trips_stg') }}
)
select
    row_number() over (order by date) as date_key,
    date,
    extract(year from date) as year,
    extract(month from date) as month,
    extract(day from date) as day,
    extract(quarter from date) as quarter,
    extract(dayofweek from date) as day_of_week,
from dates