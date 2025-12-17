# 纽约市出租车数据管道

此 GitHub Actions 工作流使用 Python 和 dbt 自动化端到端的数据管道，从初始化 Snowflake 基础设施到生成分析表和视图。

<br>
<a href="https://github.com/EliasMez/nyc-taxi-pipeline/">💻 项目源代码</a>
<br>
<a href="https://eliasmez.github.io/nyc-taxi-pipeline/dbt">📚 在线 **dbt** 文档</a>
<br>

## 📊 数据来源

[**TLC 行程记录数据**](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) - 纽约市出租车和礼车委员会

数据包含：

- 上车和下车日期/时间
- GPS 行程位置
- 距离、详细费用、支付类型
- 司机报告乘客数量

*数据由授权技术提供商收集并提供给 TLC。TLC 不保证此数据的准确性。*

## 📄 许可证

本项目采用 MIT 许可证。源数据由 [纽约市 TLC](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) 提供，并受其使用条款约束。