select
    loc_pickup.borough as pickup_borough,
    loc_dropoff.borough as dropoff_borough,
    count(*) as trip_count,
    sum(metrics.total_amount) as total_revenue,
    round(avg(metrics.total_amount), 2) as avg_revenue,
    round(avg(metrics.tip_pct), 4) as avg_tip_percentage
from {{ ref('int_trip_metrics') }} metrics
left join {{ ref('dim_locations') }} loc_pickup on metrics.pulocationid = loc_pickup.location_id
left join {{ ref('dim_locations') }} loc_dropoff on metrics.dolocationid = loc_dropoff.location_id
group by loc_pickup.borough, loc_dropoff.borough
order by total_revenue desc
