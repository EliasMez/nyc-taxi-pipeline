SELECT
    VENDORID,
    TO_TIMESTAMP_NTZ(tpep_pickup_datetime / 1000000) AS tpep_pickup_datetime,
    TO_TIMESTAMP_NTZ(tpep_dropoff_datetime / 1000000) AS tpep_dropoff_datetime,
    PASSENGER_COUNT,
    TRIP_DISTANCE,
    RATECODEID,
    STORE_AND_FWD_FLAG,
    PULOCATIONID,
    DOLOCATIONID,
    TRIM(PAYMENT_TYPE) as PAYMENT_TYPE,
    CAST(FARE_AMOUNT AS DECIMAL(10,2)) as FARE_AMOUNT,
    EXTRA,
    MTA_TAX,
    TIP_AMOUNT,
    TOLLS_AMOUNT,
    IMPROVEMENT_SURCHARGE,
    TOTAL_AMOUNT,
    CONGESTION_SURCHARGE,
    AIRPORT_FEE,
    CBD_CONGESTION_FEE
FROM {{ source('raw', 'YELLOW_TAXI_TRIPS_RAW') }}
WHERE trip_distance >= 0
AND total_amount > 0
AND fare_amount > 0
AND tpep_pickup_datetime IS NOT NULL
AND tpep_dropoff_datetime IS NOT NULL
AND tpep_pickup_datetime < tpep_dropoff_datetime
AND pulocationid IS NOT NULL
AND dolocationid IS NOT NULL