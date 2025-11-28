
    
    

with child as (
    select pickup_time_key as from_field
    from NYC_TAXI_DW.SCHEMA_FINAL.fact_trips
    where pickup_time_key is not null
),

parent as (
    select time_key as to_field
    from NYC_TAXI_DW.SCHEMA_FINAL.dim_time
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


