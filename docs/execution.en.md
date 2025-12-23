# 💻 Project Setup

## 📋 Prerequisites

- **Snowflake** account with **SECURITYADMIN** and **SYSADMIN** privileges
- **GitHub** repository with **configured secrets** (see configuration section)
- Access to NYC Taxi data sources: **https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page**
<br>

## 🚀 Execution
- Automatic: Every 1st of the month at 10:00 AM
- Manual: Via GitHub Actions interface
<br>

## ⚙️ Configuration
1. **Fork** this repository: https://github.com/EliasMez/nyc-taxi-pipeline
<br>

2. **Add the MANDATORY secrets:** `Settings` > `Secrets and variables` > `Actions` > `Secrets` > `New repository secret` <br>

| Secret | Description |
|--------|-------------|
| `SNOWFLAKE_USER` | Snowflake username |
| `SNOWFLAKE_PASSWORD` | Snowflake user password |
| `SNOWFLAKE_ACCOUNT` | Snowflake account identifier |
| `PASSWORD_DEV` | Development user password |
<br>

3. **Customize the OPTIONAL variables:** `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

| Variable | Description | Default Value |
|----------|-------------|-------------------|
| `WH_NAME` | Data warehouse name | `NYC_WH` |
| `DW_NAME` | Database name | `NYC_TAXI_DW` |
| `RAW_SCHEMA` | Raw data schema | `RAW` |
| `STAGING_SCHEMA` | Cleaned data schema | `STAGING` |
| `FINAL_SCHEMA` | Final data schema | `FINAL` |
| `PARQUET_FORMAT` | Parquet file format | `PARQUET_FORMAT` |
| `COMPUTE_SIZE` | Computing power of the data warehouse | `X-SMALL` |
| `ROLE_TRANSFORMER` | Role for transformations | `TRANSFORMER` |
| `USER_DEV` | Development user | `USER_DEV` |
| `METADATA_TABLE` | Metadata table | `FILE_LOADING_METADATA` |
| `RAW_TABLE` | Raw data table | `YELLOW_TAXI_TRIPS_RAW` |
| `STAGING_TABLE` | Staging table | `YELLOW_TAXI_TRIPS_STG` |
| `LOGGER_LEVEL` | Logging level | `INFO` |
| `SCRAPING_YEAR` | Scraping start date (>2000 and <current year)| current year |
| `TIMEZONE` | Timezone defining the offset from UTC | `UTC` |
| `GH_RELEASE_TOKEN` | GitHub token for automatic versioning (required only if using the Release workflow) | ⚠️ not defined |
<br>

⚠️ **Release Workflow (Semantic Release)**
The **Release** workflow requires a GitHub token (`GH_RELEASE_TOKEN`) to function.
If this token is not defined, **the workflow will systematically fail** during the publishing step.

**Option 1**: Disable the *Release* workflow
If you do not need automatic code versioning: `Actions` → `Release` → **Disable workflow**

**Option 2**: Create a Personal Access Token (recommended if keeping the workflow)
1. Go to: `Settings` → `Developer settings` → `Personal access tokens` → **Tokens (classic)**
2. Create a token with `repo` permissions
3. Add it as a secret: `Settings` → `Secrets and variables` → `Actions` → **New repository secret**
   - Name: `GH_RELEASE_TOKEN`
   - Value: *your token*
<br>

## 🔧 Quick Troubleshooting
- Snowflake connection failure: Check GitHub secrets
- Scraping timeout: Verify access to source URLs
- dbt error: Consult detailed job logs
- Set the value of the `LOGGER_LEVEL` variable to `DEBUG` to see detailed logs