select
    date(tpep_pickup_datetime) as pickup_date,
    count(*) as trip_count,
    round(avg(trip_distance), 2) as avg_distance,
    sum(total_amount) as total_revenue,
    round(avg(total_amount), 2) as avg_revenue_per_trip,
    round(avg(tip_amount), 2) as avg_tip_amount,
    sum(passenger_count) as total_passengers
from {{ ref('int_trip_metrics') }}
group by date(tpep_pickup_datetime)
order by pickup_date
