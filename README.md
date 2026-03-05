# NYC Taxi Data Pipeline

An automated data pipeline (Snowflake + dbt + GitHub Actions) for ingesting and transforming NYC TLC trip record data.

[![Live Documentation](https://img.shields.io/badge/docs-live_site-brightgreen)](https://eliasmez.github.io/nyc-taxi-pipeline)
[![dbt Documentation](https://img.shields.io/badge/docs-dbt_site-FF694B)](https://eliasmez.github.io/nyc-taxi-pipeline/dbt/)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)]()
[![Snowflake](https://img.shields.io/badge/Snowflake-29B5E8?logo=snowflake&logoColor=white)]()


## 📚 Documentation
*   **Project Documentation:** Available in multiple languages (🇬🇧 English, 🇫🇷 Français, 🇨🇳 中文, 🇪🇸 Español) at [https://eliasmez.github.io/nyc-taxi-pipeline](https://eliasmez.github.io/nyc-taxi-pipeline)
*   **dbt Documentation:** Technical documentation for data models, lineage, and tests at [https://eliasmez.github.io/nyc-taxi-pipeline/dbt/](https://eliasmez.github.io/nyc-taxi-pipeline/dbt/).


## 🚀 Quick Start
1.  **Fork** this repository.
2.  Add required Snowflake secrets in `Settings > Secrets > Actions`.
3.  Trigger the `NYC Taxi Data Pipeline` workflow manually via the GitHub Actions tab.

## 📊 Source Data
[**TLC Trip Record Data**](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) - NYC Taxi & Limousine Commission.

## 🎓 Certification Deliverables

This project was built as part of a French data engineering certification.

[**E5 — Mise en situation professionnelle**](certif/E5/E5.md) covers the design and implementation of the data warehouse, including data modelling, Snowflake infrastructure setup, access management, and the full ETL pipeline from Python ingestion to dbt transformations.

[**E6 — Étude de cas**](certif/E6/E6.md) covers the ongoing operations and evolution of the warehouse, including observability, alerting, maintenance planning, backup policies, GDPR compliance, and structural model evolution.

## 📄 License
This project is licensed under the MIT License. Source data is provided by the NYC TLC under their terms of use.