SELECT *
FROM {{ source('raw', 'taxi_zone_raw') }}
