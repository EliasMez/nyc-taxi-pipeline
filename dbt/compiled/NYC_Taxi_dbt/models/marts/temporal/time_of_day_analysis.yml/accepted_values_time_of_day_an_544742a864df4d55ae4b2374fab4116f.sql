
    
    

with all_values as (

    select
        time_of_day as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_FINAL.time_of_day_analysis
    group by time_of_day

)

select *
from all_values
where value_field not in (
    'Morning','Afternoon','Evening','Night'
)


