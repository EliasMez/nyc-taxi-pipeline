select
    loc.borough,
    count(*) as trip_count,
    round(avg(metrics.total_amount), 2) as avg_revenue,
    sum(metrics.total_amount) as total_revenue,
    round(avg(metrics.trip_duration_minutes), 2) as avg_duration,
    round(avg(metrics.trip_distance), 2) as avg_distance,
    round(avg(metrics.tip_amount), 2) as avg_tip_amount,
    round(avg(metrics.tip_pct), 4) as avg_tip_percentage
from {{ ref('int_trip_metrics') }} as metrics
left join {{ ref('dim_locations') }} as loc on metrics.pulocationid = loc.location_id
group by loc.borough
order by trip_count desc
