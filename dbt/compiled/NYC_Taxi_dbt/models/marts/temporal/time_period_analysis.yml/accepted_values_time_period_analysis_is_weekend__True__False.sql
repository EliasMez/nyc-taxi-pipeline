
    
    

with all_values as (

    select
        is_weekend as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_FINAL.time_period_analysis
    group by is_weekend

)

select *
from all_values
where value_field not in (
    'True','False'
)


