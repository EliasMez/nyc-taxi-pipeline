
SELECT *
FROM NYC_TAXI_DW.SCHEMA_STAGING.yellow_taxi_trips_stg
WHERE tpep_pickup_datetime <= '2000-01-01'
