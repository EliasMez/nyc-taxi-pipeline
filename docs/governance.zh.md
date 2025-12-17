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