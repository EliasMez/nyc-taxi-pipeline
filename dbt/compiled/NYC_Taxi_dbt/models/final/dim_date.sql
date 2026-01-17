with dates as (
    select distinct date(tpep_pickup_datetime) as trip_date
    from NYC_TAXI_DW.SCHEMA_STAGING.YELLOW_TAXI_TRIPS_STG
    union distinct
    select distinct date(tpep_dropoff_datetime) as trip_date
    from NYC_TAXI_DW.SCHEMA_STAGING.YELLOW_TAXI_TRIPS_STG
)

select
    to_char(trip_date, 'YYYYMMDD')::INT as date_key,
    trip_date,
    extract(year from trip_date) as year,
    extract(month from trip_date) as month,
    extract(day from trip_date) as day,
    extract(quarter from trip_date) as quarter,
    extract(dayofweek from trip_date) as day_of_week,
    case
        when day_of_week in (1, 7) then 'Weekend'
        else 'Weekday'
    end as day_type,
    monthname(trip_date) as month_name,
    dayname(trip_date) as day_name
from dates