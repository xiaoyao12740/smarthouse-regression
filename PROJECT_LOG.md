# Project Log / 项目日志

## v0.1 - Regression Pipeline

本阶段将基础房价预测脚本升级为可复用的回归工程雏形。

This stage upgrades a basic house price script into a reusable regression engineering prototype.

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

Learning focus:

- Classification predicts categories; regression predicts continuous values.
- A saved pipeline should include both preprocessing and the model.
- Error metrics must be chosen according to the business question.

## v0.2 - Unit Display And Model Optimization

Completed:

- Added a bilingual field dictionary for human-facing outputs.
- Added RMB display values using a fixed showcase assumption: `1 USD = 6.6 RMB`.
- Added a clear exchange-rate statement in README and HTML report.
- Optimized Random Forest with limited depth and split constraints.
- Enabled compressed `joblib` model saving.
- Added automatic model comparison for Linear Regression, Ridge, and Random Forest.

Result:

- Previous model size: about `155.35 MB`.
- Optimized model size: about `10.02 MB`.
- R2 remains about `0.8051`.
- Best model in the current comparison: `random_forest`.

## v0.3 - Streamlit Prediction App

Completed:

- Added `app.py` as a local Streamlit interface.
- Reused the saved model bundle instead of duplicating training logic.
- Added manual feature inputs for house price prediction.
- Displayed raw prediction in `100k USD`, estimated USD, and estimated RMB.
- Added an explicit fixed exchange-rate note: `1 USD = 6.6 RMB`.
- Added model metrics, model comparison table, and bilingual field dictionary tabs.

## v1.0 - Portfolio Freeze

Completed:

- Added a lightweight feature importance section to the Streamlit app.
- Added Dockerfile and Docker ignore rules.
- Expanded README with project positioning, business caveats, Docker usage, model comparison, screenshot guidance, and known limits.
- Confirmed the project can be treated as a v1.0 showcase version.
