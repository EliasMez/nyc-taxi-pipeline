with date_info as (
    select
        *,
        extract(dayofweek from pickup_date) + 1 as day_of_week,
        coalesce(day_of_week in (1, 7), false) as is_weekend
    from NYC_TAXI_DW.SCHEMA_STAGING.int_trip_metrics
)

select
    day_of_week,
    is_weekend,
    count(*) as trip_count,
    sum(total_amount) as total_revenue,
    round(avg(total_amount), 2) as avg_revenue,
    round(avg(trip_duration_minutes), 2) as avg_duration,
    round(avg(trip_distance), 2) as avg_distance,
    round(avg(avg_speed_mph), 2) as avg_speed,
    round(avg(tip_amount), 2) as avg_tip_amount,
    round(avg(tip_pct), 4) as avg_tip_pct
from date_info
group by day_of_week, is_weekend
order by day_of_week