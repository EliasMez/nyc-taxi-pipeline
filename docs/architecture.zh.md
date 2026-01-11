# 🏛️ 架构

## 🏗️ 技术架构

[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)]()
[![Snowflake](https://img.shields.io/badge/Snowflake-数据仓库-29B5E8?logo=snowflake&logoColor=white)]()
[![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)]()
[![dbt](https://img.shields.io/badge/dbt-数据转换-FF694B?logo=dbt&logoColor=white)]()

- **编排工具**: GitHub Actions
- **数据仓库**: Snowflake
- **数据转换**: dbt
- **编程语言**: Python
<br>

## 📁 项目结构
```bash
nyc-taxi-pipeline/
├── .github/
│   ├── workflows/
│   │   ├── nyc_taxi_pipeline.yml
│   │   ├── codeql.yml
│   │   ├── python_code_tests.yml
│   │   ├── release.yml
│   │   └── sqlfluff.yml
│   │
│   └── dependabot.yml
│
├── docs/
│
├── snowflake_ingestion/
│   ├── init_data_warehouse.py
│   ├── scrape_links.py
│   ├── upload_stage.py
│   ├── load_to_table.py
│   │
│   ├── sql/
│   │   ├── init/
│   │   ├── scraping/
│   │   ├── stage/
│   │   └── load/
│   │
│   └── tests/
│
└── dbt_transformations/
    └── NYC_Taxi_dbt/
        └── models/
            ├── staging/
            ├── final/
            └── marts/
```
<br>

## 📊 数据处理流程

### 主要流程

**纽约出租车数据管道**
每月执行的数据摄取管道：
<br>

1. **Snowflake 基础设施初始化**
   初始化 Snowflake 基础设施（数据库、模式、仓库、角色、用户）。
2. **抓取链接**
   抓取并获取源链接。
3. **上传到 Stage**
   将原始文件上传到 Snowflake Stage。
4. **加载到表**
   将数据加载到 RAW 模式的表中。
5. **运行 dbt 转换**
   执行 dbt 转换（STAGING 然后是 FINAL）。
6. **运行 dbt 测试**
   执行 dbt 测试以验证模型。

### 质量流程

- **CodeQL 安全扫描**
  使用 CodeQL 对 Python 代码进行静态分析，以检测每次推送或拉取请求到 `dev` 和 `main` 时的漏洞。
- **Dependabot 更新**
  每季度自动更新 Python 和 GitHub Actions 依赖项。
- **页面构建与部署**
  通过 GitHub Pages 自动部署项目文档。
- **Python 代码测试**
  在每次推送或拉取请求到 `dev` 和 `main` 时执行 Pytest 单元测试。
- **版本发布**
  通过 Python Semantic Release 自动进行版本控制、生成变更日志和发布版本，每次推送或拉取请求到 `main` 时触发。
- **SQL 代码质量**
  使用 SQLFluff 对 SQL 代码（dbt 模型和 Snowflake 脚本）进行自动 linting，每次推送或拉取请求到 `dev` 和 `main` 时执行。
``


## 数据建模 (Data Modeling)

此表记录了**数据的存储方式**。

| 表名称                    | 模式             | 表类型    | 物化方式  |
| :----------------------- | :---------------| :------- | :--------|
| FILE_LOADING_METADATA    | `SCHEMA_RAW`    | 瞬态表    | 表       |
| YELLOW_TAXI_TRIPS_RAW    | `SCHEMA_RAW`    | 瞬态表    | 增量      |
| TAXI_ZONE_LOOKUP         | `SCHEMA_RAW`    | 永久表    | 表       |
| TAXI_ZONE_STG            | `SCHEMA_STG`    | 永久表    | 表       |
| YELLOW_TAXI_TRIPS_STG    | `SCHEMA_STG`    | 瞬态表    | 增量      |
| int_trip_metrics         | `SCHEMA_STG`    |          | 视图      |
| fact_trips               | `SCHEMA_FINAL`  | 永久表    | 增量      |
| dim_locations            | `SCHEMA_FINAL`  | 永久表    | 表        |
| dim_time                 | `SCHEMA_FINAL`  | 永久表    | 表        |
| dim_date                 | `SCHEMA_FINAL`  | 永久表    | 表        |
| marts                    | `SCHEMA_FINAL`  |          | 视图      |

详细内容可查阅 <a href="https://eliasmez.github.io/nyc-taxi-pipeline/dbt">📚 在线 <strong>dbt</strong> 文档</a>