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
| `PASSWORD_BI` | BI Analyst user password |
| `PASSWORD_DS` | Data Scientist user password |
| `PASSWORD_MC` | Mart Consumer user password |
| `GH_RELEASE_TOKEN` | GitHub token for automatic versioning (required only if using the Release workflow) |
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
| `ROLE_BI_ANALYST` | BI Analyst role name | `ROLE_BI_ANALYST` |
| `ROLE_DATA_SCIENTIST` | Data Scientist role name | `ROLE_DATA_SCIENTIST` |
| `ROLE_MART_CONSUMER` | Mart Consumer role name | `ROLE_MART_CONSUMER` |
| `USER_DEV` | Development user | `USER_DEV` |
| `USER_BI_ANALYST` | BI Analyst username | `USER_BI_ANALYST` |
| `USER_DATA_SCIENTIST` | Data Scientist username | `USER_DATA_SCIENTIST` |
| `USER_MART_CONSUMER` | Mart Consumer username | `USER_MART_CONSUMER` |
| `METADATA_TABLE` | Metadata table | `FILE_LOADING_METADATA` |
| `RAW_TABLE` | Raw data table | `YELLOW_TAXI_TRIPS_RAW` |
| `STAGING_TABLE` | Staging table | `YELLOW_TAXI_TRIPS_STG` |
| `LOGGER_LEVEL` | Logging level | `INFO` |
| `SCRAPING_YEAR` | Scraping start date (>2000 and <current year)| current year |
| `TIMEZONE` | Timezone defining the offset from UTC | `UTC` |
| `RETENTION_DAYS` | Retention period for table change history (Time Travel) (0-90) | `1` |
| `FULL_BACKUP_POLICY_DAYS` | Full database backup retention duration | `180` |
| `RAW_TABLE_BACKUP_POLICY_DAYS` | RAW table backup retention duration | `730` |
| `FINAL_SCHEMA_BACKUP_POLICY_DAYS` | FINAL schema backup retention duration | `90` |
<br>

⚠️ **Important considerations regarding `RETENTION_DAYS`:**
*   Not applicable to **Temporary tables** (deleted at the end of a session).
*   **Fail-safe** is a protection period that begins after Time Travel expires. It is not affected by this setting.

**Error behavior and limits**
*   ⚠️ **Automatic capping (transient tables)**: Any `RETENTION_DAYS` value > 1 is treated as **1 day**.
*   ❌ **Limit exceeded error**: Any `RETENTION_DAYS` value exceeding the **allowed limit** for the account and table type will generate an error.

### **Standard Account**
*   **Transient and permanent tables**: `RETENTION_DAYS` = **0 or 1 day**.
*   **Fail-safe**: Fixed **7 days** after Time Travel.

### **Enterprise, Business Critical, and Virtual Private Snowflake Accounts**
*   **Transient tables**: `RETENTION_DAYS` = **0 or 1 day**.
*   **Permanent tables**: `RETENTION_DAYS` = **0 to 90 days**.
*   **Fail-safe**: **7 days** after Time Travel. Can be **extended up to 90 days** via a specific contract with Snowflake.
<br>


## 🔧 Quick Troubleshooting
- Snowflake connection failure: Check GitHub secrets
- Scraping timeout: Verify access to source URLs
- dbt error: Consult detailed job logs
- Set the value of the `LOGGER_LEVEL` variable to `DEBUG` to see detailed logs