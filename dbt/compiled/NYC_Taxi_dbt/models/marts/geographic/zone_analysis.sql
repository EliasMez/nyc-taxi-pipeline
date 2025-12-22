select
    loc.zone_name,
    loc.borough,
    count(*) as trip_count,
    round(avg(metrics.total_amount), 2) as avg_revenue,
    sum(metrics.total_amount) as total_revenue,
    round(avg(metrics.trip_duration_minutes), 2) as avg_duration,
    round(avg(metrics.trip_distance), 2) as avg_distance
from NYC_TAXI_DW.SCHEMA_STAGING.int_trip_metrics as metrics
left join NYC_TAXI_DW.SCHEMA_FINAL.dim_locations as loc on metrics.pulocationid = loc.location_id
group by loc.zone_name, loc.borough
order by trip_count desc