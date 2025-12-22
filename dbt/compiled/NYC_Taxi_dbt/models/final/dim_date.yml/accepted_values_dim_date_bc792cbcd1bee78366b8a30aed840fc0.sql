
    
    

with all_values as (

    select
        month_name as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_FINAL.dim_date
    group by month_name

)

select *
from all_values
where value_field not in (
    'Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'
)


