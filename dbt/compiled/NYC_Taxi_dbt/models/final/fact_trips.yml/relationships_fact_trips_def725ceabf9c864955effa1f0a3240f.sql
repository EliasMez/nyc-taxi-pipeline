
    
    

with child as (
    select pickup_location_id as from_field
    from NYC_TAXI_DW.SCHEMA_FINAL.fact_trips
    where pickup_location_id is not null
),

parent as (
    select location_id as to_field
    from NYC_TAXI_DW.SCHEMA_FINAL.dim_locations
)

select
    from_field

from child
left join parent
    on child.from_field = parent.to_field

where parent.to_field is null


