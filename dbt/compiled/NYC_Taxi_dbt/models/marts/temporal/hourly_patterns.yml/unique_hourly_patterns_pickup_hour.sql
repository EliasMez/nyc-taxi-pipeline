
    
    

select
    pickup_hour as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.hourly_patterns
where pickup_hour is not null
group by pickup_hour
having count(*) > 1


