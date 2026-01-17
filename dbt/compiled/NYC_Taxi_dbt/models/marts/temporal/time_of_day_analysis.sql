select
    case
        when pickup_hour between 6 and 11 then 'Morning'
        when pickup_hour between 12 and 17 then 'Afternoon'
        when pickup_hour between 18 and 23 then 'Evening'
        else 'Night'
    end as time_of_day,
    count(*) as trip_count,
    round(avg(total_amount), 2) as avg_revenue,
    round(avg(trip_duration_minutes), 2) as avg_duration,
    round(avg(tip_amount), 2) as avg_tip
from NYC_TAXI_DW.SCHEMA_STAGING.int_trip_metrics
group by time_of_day
order by trip_count desc