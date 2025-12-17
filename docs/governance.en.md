# 📈 Data Governance

[![CodeQL](https://img.shields.io/badge/CodeQL-Security-0078D7?logo=github&logoColor=white)]()
[![Dependabot](https://img.shields.io/badge/Dependabot-Security-025E8C?logo=dependabot&logoColor=white)]()
[![Semantic Release](https://img.shields.io/badge/Semantic_Release-Versioning-494949?logo=semantic-release&logoColor=white)]()
[![SQLFluff](https://img.shields.io/badge/SQLFluff-Linting-000000?logo=sqlfluff&logoColor=white)]()

## 📊 Monitoring
- Detailed logs in GitHub Actions.
- Email alerts in case of workflow failure or cancellation.
- Status tracking via a metadata table indicating each stage (*scraped / staged / success / failed*).

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