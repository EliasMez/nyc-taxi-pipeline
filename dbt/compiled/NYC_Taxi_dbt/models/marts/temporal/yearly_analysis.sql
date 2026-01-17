with yearly_data as (
    select
        extract(year from pickup_date) as year,
        count(*) as trip_count,
        sum(total_amount) as total_revenue
    from NYC_TAXI_DW.SCHEMA_STAGING.int_trip_metrics
    group by extract(year from pickup_date)
),

growth_data as (
    select
        year,
        trip_count,
        total_revenue,
        lag(total_revenue) over (order by year) as prev_year_revenue,
        case
            when prev_year_revenue is not null
                then round((total_revenue - prev_year_revenue) / prev_year_revenue, 4)
        end as yoy_growth
    from yearly_data
)

select
    year,
    trip_count,
    total_revenue,
    yoy_growth
from growth_data
order by year