
    
    

select
    week_start as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.weekly_analysis
where week_start is not null
group by week_start
having count(*) > 1


