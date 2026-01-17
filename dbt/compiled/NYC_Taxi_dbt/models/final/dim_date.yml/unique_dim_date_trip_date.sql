
    
    

select
    trip_date as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.dim_date
where trip_date is not null
group by trip_date
having count(*) > 1


