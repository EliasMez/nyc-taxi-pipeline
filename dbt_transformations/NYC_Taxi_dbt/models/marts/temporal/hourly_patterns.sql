select
    pickup_hour,
    count(*) as trip_count,
    sum(total_amount) as total_revenue,
    round(avg(avg_speed_mph), 2) as avg_speed,
    round(avg(trip_duration_minutes), 2) as avg_duration_minutes,
    round(avg(fare_amount), 2) as avg_fare
from {{ ref('int_trip_metrics') }}
group by pickup_hour
order by pickup_hour