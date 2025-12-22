
    
    

select
    year as unique_field,
    count(*) as n_records

from NYC_TAXI_DW.SCHEMA_FINAL.yearly_analysis
where year is not null
group by year
having count(*) > 1


