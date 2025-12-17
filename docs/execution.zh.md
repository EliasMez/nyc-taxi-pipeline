# 💻 项目启动

## 📋 先决条件

- 具有 **SECURITYADMIN** 和 **SYSADMIN** 权限的 **Snowflake** 账户
- 包含 **已配置密钥** 的 **GitHub** 仓库（见配置部分）
- 访问 NYC Taxi 数据源：**https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page**
<br>

## 🚀 执行
- 自动：每月 1 日上午 10:00
- 手动：通过 GitHub Actions 界面
<br>

## ⚙️ 配置
1. **复刻** 此仓库：https://github.com/EliasMez/nyc-taxi-pipeline
<br>

2. **添加 必需 的密钥：** `Settings` > `Secrets and variables` > `Actions` > `Secrets` > `New repository secret` <br>

| Secret | 描述 |
|--------|-------------|
| `SNOWFLAKE_USER` | Snowflake 用户名 |
| `SNOWFLAKE_PASSWORD` | Snowflake 用户密码 |
| `SNOWFLAKE_ACCOUNT` | Snowflake 账户标识符 |
| `PASSWORD_DEV` | 开发用户密码 |
<br>

3. **自定义 可选 变量：** `Settings` > `Secrets and variables` > `Actions` > `Variables` > `New repository variables` <br>

| 变量 | 描述 | 默认值 |
|----------|-------------|-------------------|
| `WH_NAME` | 数据仓库名称 | `NYC_WH` |
| `DW_NAME` | 数据库名称 | `NYC_TAXI_DW` |
| `RAW_SCHEMA` | 原始数据模式 | `RAW` |
| `STAGING_SCHEMA` | 已清理数据模式 | `STAGING` |
| `FINAL_SCHEMA` | 最终数据模式 | `FINAL` |
| `PARQUET_FORMAT` | Parquet 文件格式 | `PARQUET_FORMAT` |
| `ROLE_TRANSFORMER` | 转换角色 | `TRANSFORMER` |
| `USER_DEV` | 开发用户 | `USER_DEV` |
| `METADATA_TABLE` | 元数据表 | `FILE_LOADING_METADATA` |
| `RAW_TABLE` | 原始数据表 | `YELLOW_TAXI_TRIPS_RAW` |
| `STAGING_TABLE` | 暂存表 | `YELLOW_TAXI_TRIPS_STG` |
| `LOGGER_LEVEL` | 日志记录级别 | `INFO` |
| `SCRAPING_YEAR` | 抓取开始日期 (>2000 且 <当前年份)| 当前年份 |
| `TIMEZONE` | 定义与 UTC 偏移的时区 | `UTC` |
| `GH_RELEASE_TOKEN` | 用于自动版本控制的 GitHub 令牌（仅在需要使用 Release 工作流时） | ⚠️ 未定义 |
<br>

⚠️ **发布工作流（语义化发布）**
**发布** 工作流需要一个 GitHub 令牌（`GH_RELEASE_TOKEN`）才能运行。
如果未定义此令牌，**工作流将在发布步骤中系统性地失败**。

**选项 1**：禁用 *Release* 工作流
如果您不需要自动代码版本控制：`Actions` → `Release` → **Disable workflow**

**选项 2**：创建个人访问令牌（推荐，如果要保留该工作流）
1. 前往：`Settings` → `Developer settings` → `Personal access tokens` → **Tokens (classic)**
2. 创建一个具有 `repo` 权限的令牌
3. 将其添加为密钥：`Settings` → `Secrets and variables` → `Actions` → **New repository secret**
   - 名称：`GH_RELEASE_TOKEN`
   - 值：*您的令牌*
<br>

## 🔧 快速故障排除
- Snowflake 连接失败：检查 GitHub 密钥
- 抓取超时：验证对源 URL 的访问
- dbt 错误：查看详细的作业日志
- 将 `LOGGER_LEVEL` 变量的值设置为 `DEBUG` 以查看详细日志