# Changelog

## v1.0

- Added Streamlit inference interface for manual prediction.
- Added model metrics, model comparison, and field dictionary views.
- Added input-unit conversion for median income.
- Added output display in model units, USD, and RMB.
- Added feature-importance ranking and chart exports.
- Added Docker configuration for local deployment.
- Optimized Random Forest persistence to keep the model artifact compact.
- Expanded public documentation with project scope, assumptions, usage, and limitations.

中文说明：

- 增加 Streamlit 推理界面，支持手动预测
- 增加模型指标、模型对比和字段说明视图
- 增加收入输入单位换算
- 增加模型单位、美元和人民币结果展示
- 增加特征重要性排序和图表导出
- 增加 Docker 本地部署配置
- 优化 Random Forest 模型保存，压缩模型文件体积
- 补充公开文档中的项目范围、假设、用法和限制

## v0.2

- Added a bilingual field dictionary for user-facing feature descriptions.
- Added fixed RMB display conversion with an explicit exchange-rate assumption.
- Added automatic comparison across Linear Regression, Ridge, and Random Forest.
- Reduced the saved model size from about `155.35 MB` to about `10.02 MB`.

中文说明：

- 增加面向用户展示的中英文字段说明
- 增加人民币展示换算，并明确固定汇率假设
- 增加 Linear Regression、Ridge 和 Random Forest 自动对比
- 将保存后的模型文件从约 `155.35 MB` 压缩到约 `10.02 MB`

## v0.1

- Established the regression project structure.
- Added config-driven paths for data, models, and outputs.
- Added data preparation, preprocessing, training, evaluation, prediction export, and HTML reporting.

中文说明：

- 建立回归项目结构
- 使用配置文件管理数据、模型和输出路径
- 增加数据准备、预处理、训练、评估、预测导出和 HTML 报告
