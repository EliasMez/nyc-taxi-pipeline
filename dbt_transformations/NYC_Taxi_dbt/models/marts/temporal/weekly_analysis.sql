select
    date_trunc('week', pickup_date) as week_start,
    count(*) as trip_count,
    sum(total_amount) as total_revenue,
    round(avg(total_amount), 2) as avg_revenue,
    round(avg(trip_distance), 2) as avg_distance,
    round(avg(trip_duration_minutes), 2) as avg_duration,
    round(avg(tip_amount), 2) as avg_tip,
    round(avg(tip_pct), 4) as avg_tip_pct
from {{ ref('int_trip_metrics') }}
group by date_trunc('week', pickup_date)
order by week_start
