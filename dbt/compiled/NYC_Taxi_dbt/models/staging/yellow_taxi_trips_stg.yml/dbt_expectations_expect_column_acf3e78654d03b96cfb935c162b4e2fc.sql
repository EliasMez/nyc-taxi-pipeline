





    with grouped_expression as (
    select
        
        
    
  tpep_dropoff_datetime > tpep_pickup_datetime as expression


    from NYC_TAXI_DW.SCHEMA_STAGING.YELLOW_TAXI_TRIPS_STG
    

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




