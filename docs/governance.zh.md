# 📈 数据治理

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 监控

### 日志级别
日志级别可通过 GitHub Actions 变量 `LOGGER_LEVEL` 配置（默认：`INFO`）。

| 级别 | 用途 |
|------|------|
| `CRITICAL` | 不可恢复的系统故障 |
| `ERROR` | 严重错误（连接、加载、无效值） |
| `WARNING` | 非阻塞警报（无文件可加载、文件已引用） |
| `INFO` | 进度信息（步骤开始/结束、加载的文件数和行数） |
| `DEBUG` | 执行的 SQL 查询、元数据更新、OpenTelemetry 追踪 |

日志可在 GitHub Actions 中查看。工作流失败或取消时发送电子邮件警报。

### 摄取跟踪
`FILE_LOADING_METADATA` 表在整个管道中跟踪每个文件的状态。

| 状态 | 含义 |
|------|------|
| `SCRAPED` | 文件已检测，等待上传 |
| `STAGED` | 文件已上传至 Stage |
| `SUCCESS` | 加载成功 |
| `FAILED_STAGE` | 上传至 Stage 失败 |
| `FAILED_LOAD` | 加载到表失败 |

## ✅ 数据质量
- **dbt** 测试确保数据的完整性、一致性和有效性。
- 通过系统的元数据验证进行重复项管理。

## 🧪 代码质量
- 使用 **Pytest** 进行单元测试。
- 使用 **SQLFluff** 进行 SQL 验证。
- 使用文档字符串和文档测试进行函数文档记录。
- <a href="https://eliasmez.github.io/nyc-taxi-pipeline/docstrings/">📚 技术文档</a>

## 🔐 安全
- 日志中的密钥加密。
- 使用 **GitHub Secrets**。
- 在 Snowflake 中应用最小权限原则。
- 使用 **CodeQL** 进行静态分析。
- 通过 **Dependabot** 进行自动安全更新。

## 👥 访问权限与角色管理

数据仓库的访问基于**最小权限原则**：每个角色仅拥有完成其职能所必需的权限。

### Snowflake 系统角色

由平台预定义，仅在基础设施初始化期间使用：

| 角色 | 用途 |
|------|------|
| `SYSADMIN` | 创建 warehouse、数据库和模式；授予权限 |
| `SECURITYADMIN` | 创建业务角色和用户账户 |
| `ACCOUNTADMIN` | 配置 Time Travel |

### 业务角色

| 角色 | 用户 | 访问权限 | 使用场景 |
|------|------|---------|---------|
| **TRANSFORMER** | USER_DEV | 所有模式 | dbt ETL 管道和 Python 数据摄取 |
| **BI_ANALYST** | USER_BI_ANALYST | 读取 SCHEMA_FINAL（表 + 视图） | BI 报表 |
| **DATA_SCIENTIST** | USER_DATA_SCIENTIST | 读取 SCHEMA_STAGING + SCHEMA_FINAL（仅表） | 探索性分析 |
| **MART_CONSUMER** | USER_MART_CONSUMER | 仅读取 SCHEMA_FINAL 视图 | 消费分析聚合 |

## 📋 服务水平指标（SLA）

### Snowflake SLA（供应商）

两个月度可用性阈值同时适用：

| 阈值 | 条件 | 违约金 |
|------|------|--------|
| **99.9%** | 中断 > 43 分钟或 > 1% 错误 | 10%（< 99.9%）→ 25%（< 99.0%）→ 50%（< 95.0%） |
| **99.99%** | 短暂中断（4–43 分钟，> 10% 错误）累计 > 43 分钟 | 违反 99.9% 阈值 |

### 项目 SLA

| 指标 | 目标 |
|------|------|
| 月度管道执行时长 | < 30 分钟 |
| 数据加载成功率 | 100% |
| dbt 测试通过率 | 100% |
| 数据新鲜度 | < 30 天 |
| P1 事件解决时间 | < 48 小时 |

## 💾 数据备份

**Snowflake Time Travel**（Standard 账户 1 天）允许恢复近期更改，但不是备份：不会创建独立副本。以下策略确保在独立副本上进行长期保留。

| 对象 | 频率 | 保留期 |
|------|------|--------|
| 完整数据库 `NYC_TAXI_DW` | 每月 | 180 天 |
| 表 `YELLOW_TAXI_TRIPS_RAW` | 每月 | **730 天** |
| `FINAL` 模式 | 每月 | 90 天 |

- **730 天**用于 RAW 表：如果 NYC TLC 网站不再保留历史记录，源数据将无法恢复。
- **180 天**用于完整数据库：中间时长，覆盖多个分析周期，同时避免过高的存储成本。
- **90 天**用于 FINAL 模式：可通过 dbt 从 RAW 重建。
- 可通过变量 `RAW_TABLE_BACKUP_POLICY_DAYS`、`FULL_BACKUP_POLICY_DAYS`、`FINAL_SCHEMA_BACKUP_POLICY_DAYS` 配置保留期限。
## 🔒 GDPR 合规

### 个人数据处理

| 处理 | 数据 | 目的 | 法律依据 | 保留期 |
|-----|------|------|---------|--------|
| 行程数据 | 无直接可识别数据* | 统计分析 | 合法利益 | 按备份策略 |
| 位置信息 | 区域（LocationID）、时间戳 | 地理和时间分析 | 合法利益 | 按备份策略 |
| 文档分析 | 通过 Google Analytics 的导航数据 | 受众衡量 | 同意 | 2 个月 |

*NYC TLC 数据不包含姓名、驾照号码或地址。位置以区域表示，而非精确的 GPS 坐标。*

### Cookies
文档使用 **Google Analytics (GA4)**（明确同意后启用，保留 2 个月）和 **GitHub** 小部件（功能性 Cookie，不收集个人数据）。可随时通过页面底部的 *"Change cookie settings"* 修改选择。
