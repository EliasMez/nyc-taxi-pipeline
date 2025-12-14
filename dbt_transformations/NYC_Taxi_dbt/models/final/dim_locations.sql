select
    locationid::NUMBER(10, 2) as location_id,
    borough::VARCHAR(55) as borough,
    zone::VARCHAR(55) as zone_name,
    service_zone::VARCHAR(55) as service_zone
from {{ ref('taxi_zone_lookup') }}
