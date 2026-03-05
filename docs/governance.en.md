# 📈 Data Governance

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 Monitoring

### Log Levels
The log level is configurable via the GitHub Actions variable `LOGGER_LEVEL` (default: `INFO`).

| Level | Usage |
|-------|-------|
| `CRITICAL` | Unrecoverable system failures |
| `ERROR` | Critical errors (connection, loading, invalid values) |
| `WARNING` | Non-blocking alerts (no file to load, file already referenced) |
| `INFO` | Progress (step start/end, number of files and rows loaded) |
| `DEBUG` | SQL queries executed, metadata updates, OpenTelemetry traces |

Logs viewable in GitHub Actions. Email alerts on workflow failure or cancellation.

### Ingestion Tracking
The `FILE_LOADING_METADATA` table tracks the status of each file throughout the pipeline.

| Status | Meaning |
|--------|---------|
| `SCRAPED` | File detected, awaiting upload |
| `STAGED` | File uploaded to stage |
| `SUCCESS` | Load successful |
| `FAILED_STAGE` | Upload to stage failed |
| `FAILED_LOAD` | Table load failed |

## ✅ Data Quality
- **dbt** tests ensuring data integrity, consistency, and validity.
- Duplicate management through systematic metadata verification.

## 🧪 Code Quality
- Unit tests with **Pytest**.
- SQL validation with **SQLFluff**.
- Docstrings and doctests for function documentation.
- <a href="https://eliasmez.github.io/nyc-taxi-pipeline/docstrings/">📚 Technical documentation</a>

## 🔐 Security
- Secrets encrypted in logs.
- Use of **GitHub Secrets**.
- Minimal permissions applied in Snowflake.
- Static analysis with **CodeQL**.
- Automated security updates via **Dependabot**.

## 👥 Access and Role Management

Access to the warehouse is based on the **principle of least privilege**: each role has only the rights strictly necessary for its function.

### Snowflake System Roles

Predefined by the platform, used only during infrastructure initialization:

| Role | Usage |
|------|-------|
| `SYSADMIN` | Creates the warehouse, database, and schemas; grants privileges |
| `SECURITYADMIN` | Creates business roles and user accounts |
| `ACCOUNTADMIN` | Configures Time Travel |

### Business Roles

| Role | User | Access | Use Case |
|------|------|--------|----------|
| **TRANSFORMER** | USER_DEV | All schemas | dbt ETL pipeline and Python ingestion |
| **BI_ANALYST** | USER_BI_ANALYST | Read SCHEMA_FINAL (tables + views) | BI reports |
| **DATA_SCIENTIST** | USER_DATA_SCIENTIST | Read SCHEMA_STAGING + SCHEMA_FINAL (tables) | Exploratory analysis |
| **MART_CONSUMER** | USER_MART_CONSUMER | Read SCHEMA_FINAL views only | Consumption of analytical aggregates |

## 📋 Service Level Indicators (SLA)

### Snowflake SLA (vendor)

Two monthly availability thresholds apply simultaneously:

| Threshold | Condition | Penalties |
|-----------|-----------|-----------|
| **99.9%** | Outage > 43 min or > 1% errors | 10% (< 99.9%) → 25% (< 99.0%) → 50% (< 95.0%) |
| **99.99%** | Short outages (4–43 min, > 10% errors) cumulated > 43 min | Violation of 99.9% threshold |

### Project SLA

| Indicator | Target |
|-----------|--------|
| Monthly pipeline duration | < 30 min |
| Data loading success rate | 100% |
| dbt test pass rate | 100% |
| Data freshness | < 30 days |
| P1 incident resolution | < 48 h |

## 💾 Backups

**Snowflake Time Travel** (1 day on Standard account) allows recovery of recent changes but is not a backup: no independent copy is created. The policies below ensure long-term retention on separate copies.

| Object | Frequency | Retention |
|--------|-----------|-----------|
| Full database `NYC_TAXI_DW` | Monthly | 180 days |
| Table `YELLOW_TAXI_TRIPS_RAW` | Monthly | **730 days** |
| `FINAL` schema | Monthly | 90 days |

- **730 days** for the RAW table: source data potentially irreplaceable if the NYC TLC website no longer retains history.
- **180 days** for the full database: intermediate duration covering several analysis cycles without excessive storage cost.
- **90 days** for the FINAL schema: reconstructible from RAW via dbt.
- Durations configurable via variables `RAW_TABLE_BACKUP_POLICY_DAYS`, `FULL_BACKUP_POLICY_DAYS`, `FINAL_SCHEMA_BACKUP_POLICY_DAYS`.
## 🔒 GDPR Compliance

### Personal Data Processing

| Processing | Data | Purpose | Legal Basis | Retention |
|-----------|------|---------|-------------|-----------|
| Trip data | No directly identifying data* | Statistical analysis | Legitimate interest | Per backup policy |
| Locations | Zones (LocationID), timestamps | Geographic and temporal analysis | Legitimate interest | Per backup policy |
| Documentation analytics | Navigation via Google Analytics | Audience measurement | Consent | 2 months |

*NYC TLC data contains no names, license numbers, or addresses. Locations are expressed as zones, not precise GPS coordinates.*

### Cookies
The documentation uses **Google Analytics (GA4)** after explicit consent (2-month retention) and a **GitHub** widget (functional cookie, no personal data collected). The choice can be changed at any time via *"Change cookie settings"* in the page footer.
