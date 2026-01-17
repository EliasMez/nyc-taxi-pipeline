
    
    

with all_values as (

    select
        borough as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_STAGING.taxi_zone_stg
    group by borough

)

select *
from all_values
where value_field not in (
    'Manhattan','Queens','Brooklyn','Bronx','Staten Island','EWR','Unknown','N/A'
)


