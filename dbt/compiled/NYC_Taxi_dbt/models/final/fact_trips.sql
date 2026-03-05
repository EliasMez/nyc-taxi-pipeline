with trips as (
    select
        *,
        date(tpep_pickup_datetime) as pickup_date,
        time(tpep_pickup_datetime) as pickup_time,
        date(tpep_dropoff_datetime) as dropoff_date,
        time(tpep_dropoff_datetime) as dropoff_time
    from NYC_TAXI_DW.SCHEMA_STAGING.YELLOW_TAXI_TRIPS_STG
)

select
    trips.trip_id,
    dd_pickup.date_key as pickup_date_key,
    dt_pickup.time_key as pickup_time_key,
    dd_dropoff.date_key as dropoff_date_key,
    dt_dropoff.time_key as dropoff_time_key,
    trips.pulocationid as pickup_location_id,
    trips.dolocationid as dropoff_location_id,

    trips.trip_distance,
    trips.fare_amount,
    trips.tip_amount,
    trips.total_amount,
    trips.passenger_count

from trips
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_date as dd_pickup on trips.pickup_date = dd_pickup.trip_date
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_time as dt_pickup on trips.pickup_time = dt_pickup.trip_time
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_date as dd_dropoff on trips.dropoff_date = dd_dropoff.trip_date
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_time as dt_dropoff on trips.dropoff_time = dt_dropoff.trip_time
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_locations as loc_pickup on trips.pulocationid = loc_pickup.location_id
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_locations as loc_dropoff on trips.dolocationid = loc_dropoff.location_id