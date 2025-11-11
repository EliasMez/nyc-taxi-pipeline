select
    to_date(tpep_pickup_datetime) as pickup_date,
    count(*) as trip_count,
    round(avg(trip_distance), 2) as avg_distance,
    sum(total_amount) as total_revenue
from {{ ref('int_trip_metrics') }}
group by pickup_date
order by pickup_date
