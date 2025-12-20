{% docs __overview__ %}
# NYC Taxi Data Pipeline - dbt Documentation

Welcome to the dbt documentation for the **NYC Taxi Data Pipeline** project.
This project aims to transform raw data from the NYC TLC (Taxi & Limousine Commission) into analytical tables ready for analysis and reporting.
- 📚 [Global Project Documentation](https://eliasmez.github.io/nyc-taxi-pipeline/)
- 💻 [Project Source Code](https://github.com/EliasMez/nyc-taxi-pipeline/)

## Role of dbt

The dbt workflow transforms data from the **raw layer** to the **staging layer**, which contains:
- The imported seed `taxi_zone_lookup`
- The `stg_taxi_trips` table containing cleaned raw data
- The intermediate table `int_trip_metrics` for calculated metrics

and then to the **final layer**, which contains:
- **Dimensions**
- **Fact Tables**
- **Analytical Marts**

Each dbt model is documented here, including its position in the pipeline, its description, and its relationships with other models.

## Navigating the Documentation

- **Project Tab**: Explore the structure of your dbt project and access the documentation for each model.
- **Database Tab**: Visualize the relationships between tables, facts, and dimensions as in a database explorer.
- **Graph Exploration**: View the dependency graph to follow model lineage by clicking the icon located in the **bottom right corner of the screen**.

For more information about dbt and its operation, consult [the official dbt documentation](https://docs.getdbt.com/).

---
{% enddocs %}

{% docs __source_raw__ %}
## Data Source – Raw

The source data comes from **TLC Trip Record Data** (New York City Taxi & Limousine Commission).

It notably contains:
- Pick-up and drop-off dates and times
- GPS locations of trips
- Distances traveled
- Detailed fares and payment types
- Number of passengers

The data is collected by authorized technology providers and provided to the TLC.
The TLC does not guarantee the accuracy of the data.
{% enddocs %}

{% docs __dbt_utils__ %}
## dbt_utils

The **dbt_utils** package is used in this project **for its advanced testing macros**, notably `accepted_range`, which checks that the values of a column fall within an expected range.
{% enddocs %}

{% docs __dbt_expectations__ %}
## dbt_expectations

The **dbt_expectations** package is used to implement advanced data quality tests.

It notably allows for:
- Verifying data completeness
- Controlling expected values
- Detecting statistical anomalies
- Reinforcing the reliability of analytical models

These tests ensure the quality of the produced dimensions, facts, and marts.
{% enddocs %}

{% docs __dbt_date__ %}
## dbt_date

The **dbt_date** package provides macros for date and time period manipulation.

In this project, the date and time dimensions are built manually from source data timestamps to reflect only the values actually observed. The logic is implemented in pure SQL as it meets the needs of the temporal marts (daily, weekly, monthly, hourly, yearly) without requiring a full artificial calendar.
{% enddocs %}