

with meet_condition as(
  select *
  from NYC_TAXI_DW.SCHEMA_FINAL.daily_summary
),

validation_errors as (
  select *
  from meet_condition
  where
    -- never true, defaults to an empty result set. Exists to ensure any combo of the `or` clauses below succeeds
    1 = 2
    -- records with a value >= min_value are permitted. The `not` flips this to find records that don't meet the rule.
    or not avg_revenue_per_trip >= 0
)

select *
from validation_errors

