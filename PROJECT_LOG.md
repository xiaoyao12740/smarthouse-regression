# Project Log

## v0.1 - Regression Pipeline

本阶段将基础房价预测脚本升级为可复用的回归工程雏形。

This stage upgrades a basic house-price script into a reusable regression engineering prototype.

Completed:

- Created a clean project structure.
- Added config-driven data and output paths.
- Added data preparation and sample prediction CSV generation.
- Added preprocessing with median imputation and scaling.
- Added Linear Regression, Ridge, and Random Forest models.
- Added MAE, RMSE, and R2 evaluation.
- Added model persistence with `joblib`.
- Added prediction export.
- Added visual reports and HTML report.

中文说明：

- 建立清晰的项目目录结构
- 使用配置文件管理数据路径和输出路径
- 自动准备训练数据和预测样本
- 增加中位数缺失值填充与特征标准化
- 加入 Linear Regression、Ridge、Random Forest 模型
- 使用 MAE、RMSE、R2 评估回归效果
- 通过 `joblib` 保存模型
- 导出预测结果
- 生成可视化图表和 HTML 报告

Learning focus:

- Classification predicts categories; regression predicts continuous values.
- A saved pipeline should include both preprocessing and the model.
- Error metrics must be chosen according to the business question.

学习重点：

- 分类任务预测类别，回归任务预测连续数值
- 可复用模型文件应同时保存预处理流程和模型本体
- 误差指标要结合业务问题选择，而不是只看单一分数

## v0.2 - Unit Display And Model Optimization

Completed:

- Added a bilingual field dictionary for human-facing outputs.
- Added RMB display values using a fixed showcase assumption: `1 USD = 6.6 RMB`.
- Added a clear exchange-rate statement in README and HTML report.
- Optimized Random Forest with limited depth and split constraints.
- Enabled compressed `joblib` model saving.
- Added automatic model comparison for Linear Regression, Ridge, and Random Forest.

中文说明：

- 增加面向用户展示的中英文字段说明
- 按固定展示假设 `1 USD = 6.6 RMB` 增加人民币展示值
- 在 README 和 HTML 报告中明确汇率假设
- 通过限制深度和分裂条件优化 Random Forest
- 启用压缩模型保存
- 自动对比 Linear Regression、Ridge 和 Random Forest

Result:

- Previous model size: about `155.35 MB`.
- Optimized model size: about `10.02 MB`.
- R2 remains about `0.8051`.
- Best model in the current comparison: `random_forest`.

结果：

- 优化前模型约 `155.35 MB`
- 优化后模型约 `10.02 MB`
- R2 仍保持在约 `0.8051`
- 当前对比中的最佳模型为 `random_forest`

## v0.3 - Streamlit Prediction App

Completed:

- Added `app.py` as a local Streamlit interface.
- Reused the saved model bundle instead of duplicating training logic.
- Added manual feature inputs for house-price prediction.
- Displayed raw prediction in `100k USD`, estimated USD, and estimated RMB.
- Added an explicit fixed exchange-rate note: `1 USD = 6.6 RMB`.
- Added model metrics, model comparison table, and bilingual field dictionary tabs.

中文说明：

- 增加 `app.py` 作为本地 Streamlit 交互界面
- 复用已保存的模型包，避免在页面层重复训练逻辑
- 增加手动输入特征的房价预测流程
- 同时展示 `十万美元` 原始预测值、美元估算值和人民币估算值
- 明确展示固定汇率假设 `1 USD = 6.6 RMB`
- 增加模型指标、模型对比表和字段说明标签页

## v1.0 - Portfolio Freeze

Completed:

- Added a lightweight feature importance section to the Streamlit app.
- Added Dockerfile and Docker ignore rules.
- Expanded README with project positioning, business caveats, Docker usage, model comparison, screenshot guidance, and known limits.
- Clarified that this project should use local port `8502` when running beside another Streamlit demo.
- Added an input unit conversion layer for median income.
- Replaced the vertical feature-importance chart with a horizontal chart so long labels remain readable.
- Confirmed the project can be treated as a v1.0 showcase version.

中文说明：

- 在 Streamlit 页面中加入轻量级特征重要性解释
- 增加 Dockerfile 和 Docker 忽略规则
- 扩展 README，补充项目定位、业务限制、Docker 用法、模型对比和已知限制
- 明确本项目与其他 Streamlit 示例并行运行时建议使用本地 `8502` 端口
- 增加收入输入单位换算层
- 将特征重要性图改为横向展示，提升长标签可读性
- 将当前版本整理为可用于作品集展示的 v1.0 版本
