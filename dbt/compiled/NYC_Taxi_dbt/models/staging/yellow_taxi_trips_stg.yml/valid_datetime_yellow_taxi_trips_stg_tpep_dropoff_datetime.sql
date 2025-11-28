
SELECT *
FROM NYC_TAXI_DW.SCHEMA_STAGING.yellow_taxi_trips_stg
WHERE tpep_dropoff_datetime <= '2000-01-01'
