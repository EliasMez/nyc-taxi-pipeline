
    
    

with all_values as (

    select
        day_name as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_FINAL.dim_date
    group by day_name

)

select *
from all_values
where value_field not in (
    'Mon','Tue','Wed','Thu','Fri','Sat','Sun'
)


