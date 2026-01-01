
    
    

select
    locationid as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_STAGING.taxi_zone_stg
where locationid is not null
group by locationid
having count(*) > 1


