
    
    

select
    time_of_day as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.time_of_day_analysis
where time_of_day is not null
group by time_of_day
having count(*) > 1


