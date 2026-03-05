
    
    

select
    TRIP_ID as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_SCHEMA_RAW.YELLOW_TAXI_TRIPS_RAW
where TRIP_ID is not null
group by TRIP_ID
having count(*) > 1


