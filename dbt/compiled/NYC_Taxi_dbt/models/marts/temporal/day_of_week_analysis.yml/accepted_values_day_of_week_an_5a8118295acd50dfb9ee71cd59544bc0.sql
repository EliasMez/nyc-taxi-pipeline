
    
    

with all_values as (

    select
        day_name as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_FINAL.day_of_week_analysis
    group by day_name

)

select *
from all_values
where value_field not in (
    'Sun','Mon','Tue','Wed','Thu','Fri','Sat'
)


