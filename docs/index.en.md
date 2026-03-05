# NYC Taxi Data Pipeline

This GitHub Actions workflow automates the end-to-end data pipeline, from initializing the Snowflake infrastructure to producing analytical tables and views using Python and dbt.

<br>
<a href="https://github.com/EliasMez/nyc-taxi-pipeline/">💻 Project source code</a>
<br>
<a href="https://eliasmez.github.io/nyc-taxi-pipeline/dbt">📚 Online **dbt** documentation</a>
<br>

## 📊 Data Source

[**TLC Trip Record Data**](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) - NYC Taxi and Limousine Commission

The data includes:

- Pickup and dropoff dates/times
- Pickup and dropoff zones
- Distances, detailed fares, payment types
- Passenger count reported by the driver

*The data is collected by authorized technology providers and provided to the TLC. The TLC does not guarantee the accuracy of this data.*

## 📄 License

This project is licensed under the MIT License. The source data is provided by the [NYC TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and subject to their terms of use.