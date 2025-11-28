
    
    

select
    trip_time as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.dim_time
where trip_time is not null
group by trip_time
having count(*) > 1


