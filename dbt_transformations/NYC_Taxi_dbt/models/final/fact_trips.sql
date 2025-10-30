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
    -- Clés étrangères
    dd_pickup.date_key as pickup_date_key,
    dt_pickup.time_key as pickup_time_key,
    dd_dropoff.date_key as dropoff_date_key,
    dt_dropoff.time_key as dropoff_time_key,
    loc_pickup.location_key as pickup_location_key,
    loc_dropoff.location_key as dropoff_location_key,

    -- Mesures
    trips.trip_distance,
    trips.fare_amount,
    trips.tip_amount,
    trips.total_amount,
    trips.passenger_count

from trips
left join {{ ref('dim_date') }} dd_pickup on trips.pickup_date = dd_pickup.date
left join {{ ref('dim_time') }} dt_pickup on trips.pickup_time = dt_pickup.time
left join {{ ref('dim_date') }} dd_dropoff on trips.dropoff_date = dd_dropoff.date
left join {{ ref('dim_time') }} dt_dropoff on trips.dropoff_time = dt_dropoff.time
left join {{ ref('dim_locations') }} loc_pickup on trips.pulocationid = loc_pickup.location_id
left join {{ ref('dim_locations') }} loc_dropoff on trips.dolocationid = loc_dropoff.location_id