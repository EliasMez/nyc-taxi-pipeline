select
    pulocationid,
    count(*) as trip_count,
    round(avg(total_amount),2) as avg_revenue,
    sum(total_amount) as total_revenue
from {{ ref('int_trip_metrics') }}
group by pulocationid
order by trip_count desc