
    
    

with all_values as (

    select
        service_zone as value_field,
        count(*) as n_records

    from NYC_TAXI_DW.SCHEMA_SCHEMA_RAW.taxi_zone_raw
    group by service_zone

)

select *
from all_values
where value_field not in (
    'EWR','Boro Zone','Yellow Zone','Airports','N/A'
)


