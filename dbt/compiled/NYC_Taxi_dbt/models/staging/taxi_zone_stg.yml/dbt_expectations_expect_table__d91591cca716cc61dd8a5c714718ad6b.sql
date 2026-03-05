

    with grouped_expression as (
    select
        
        
    
  
count(*) = 265
 as expression


    from NYC_TAXI_DW.SCHEMA_STAGING.taxi_zone_stg
    

),
validation_errors as (

    select
        *
    from
        grouped_expression
    where
        not(expression = true)

)

select *
from validation_errors



