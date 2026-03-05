
    
    

select
    month as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.monthly_analysis
where month is not null
group by month
having count(*) > 1


