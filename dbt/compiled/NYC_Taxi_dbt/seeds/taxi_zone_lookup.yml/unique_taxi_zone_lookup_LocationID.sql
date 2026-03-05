
    
    

select
    LocationID as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_SCHEMA_RAW.taxi_zone_raw
where LocationID is not null
group by LocationID
having count(*) > 1


