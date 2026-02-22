# 📈 数据治理

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 监控
- GitHub Actions 中的详细日志。
- 工作流失败或取消时的电子邮件警报。
- 通过元数据表跟踪每个阶段的状态（*已抓取 / 已暂存 / 成功 / 失败*）。

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
| 表 `YELLOW_TAXI_TRIPS_RAW` | 每月 | **730 天**（默认值） |
| `FINAL` 模式 | 每月 | 90 天 |

- **730 天**用于 RAW 表：如果 NYC TLC 网站不再保留历史记录，源数据将无法恢复。
- **90 天**用于 FINAL 模式：可通过 dbt 从 RAW 重建。
- 可通过变量 `RAW_TABLE_BACKUP_POLICY_DAYS`、`FULL_BACKUP_POLICY_DAYS`、`FINAL_SCHEMA_BACKUP_POLICY_DAYS` 配置保留期限。