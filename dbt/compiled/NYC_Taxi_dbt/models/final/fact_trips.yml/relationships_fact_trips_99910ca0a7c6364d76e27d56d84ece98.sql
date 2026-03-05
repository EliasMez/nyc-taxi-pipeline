
    
    

with child as (
    select dropoff_date_key as from_field
    from NYC_TAXI_DW.SCHEMA_FINAL.fact_trips
    where dropoff_date_key is not null
),

parent as (
    select date_key as to_field
    from NYC_TAXI_DW.SCHEMA_FINAL.dim_date
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


