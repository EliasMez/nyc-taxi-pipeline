select
    date_trunc('month', pickup_date) as month,
    count(*) as trip_count,
    round(avg(trip_distance), 2) as avg_distance,
    sum(total_amount) as total_revenue,
    round(avg(total_amount), 2) as avg_revenue_per_trip,
    round(avg(tip_amount), 2) as avg_tip_amount,
    sum(passenger_count) as total_passengers,
    round(avg(trip_duration_minutes), 2) as avg_duration,
    count(distinct pulocationid) as unique_pickup_locations,
    round(avg(tip_pct), 4) as avg_tip_percentage
from NYC_TAXI_DW.SCHEMA_STAGING.int_trip_metrics
group by date_trunc('month', pickup_date)
order by month