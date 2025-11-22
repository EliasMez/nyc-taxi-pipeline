with trips as (
    select
        *,
        date(tpep_pickup_datetime) as pickup_date,
        time(tpep_pickup_datetime) as pickup_time,
        date(tpep_dropoff_datetime) as dropoff_date,
        time(tpep_dropoff_datetime) as dropoff_time
    from {{ ref('yellow_taxi_trips_stg') }}
)

select
    dd_pickup.date_key as pickup_date_key,
    dt_pickup.time_key as pickup_time_key,
    dd_dropoff.date_key as dropoff_date_key,
    dt_dropoff.time_key as dropoff_time_key,
    loc_pickup.location_key as pickup_location_key,
    loc_dropoff.location_key as dropoff_location_key,

    trips.trip_distance,
    trips.fare_amount,
    trips.tip_amount,
    trips.total_amount,
    trips.passenger_count

from trips
left join {{ ref('dim_date') }} as dd_pickup on trips.pickup_date = dd_pickup.trip_date
left join {{ ref('dim_time') }} as dt_pickup on trips.pickup_time = dt_pickup.trip_time
left join {{ ref('dim_date') }} as dd_dropoff on trips.dropoff_date = dd_dropoff.trip_date
left join {{ ref('dim_time') }} as dt_dropoff on trips.dropoff_time = dt_dropoff.trip_time
left join {{ ref('dim_locations') }} as loc_pickup on trips.pulocationid = loc_pickup.location_id
left join {{ ref('dim_locations') }} as loc_dropoff on trips.dolocationid = loc_dropoff.location_id
