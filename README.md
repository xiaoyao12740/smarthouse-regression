# SmartHouse Regression / Intelligent House Price Prediction

SmartHouse Regression is a lightweight machine learning application for tabular regression and business-style house price prediction. It combines data preparation, model comparison, optimized model persistence, bilingual field presentation, unit conversion, explainability, and a Streamlit inference interface.

SmartHouse Regression 是一个面向表格回归预测场景的轻量级机器学习应用，覆盖数据准备、模型比较、模型压缩保存、双语字段展示、单位换算、预测解释和 Streamlit 推理页面。

## Positioning / 项目定位

The project is built on the California Housing dataset and demonstrates how a regression model can be packaged into a usable prediction system. It does not claim to predict real Chinese housing prices. RMB values are provided only as a presentation conversion using a fixed assumption: `1 USD = 6.6 RMB`.

本项目基于 California Housing 数据集，展示如何将回归模型封装为可交互的预测系统。项目不声称预测真实中国房价；人民币结果仅用于展示换算，固定假设为 `1 USD = 6.6 RMB`。

## Highlights / 项目亮点

- Config-driven regression pipeline
- CSV data preparation and sample prediction data
- Median imputation and feature scaling
- Linear Regression, Ridge, and Random Forest comparison
- Optimized Random Forest model size: about `10.02 MB`
- Streamlit prediction interface
- Income unit conversion before inference
- USD and RMB display conversion after prediction
- Feature importance explanation with share percentages
- Downloadable CSV and transparent SVG report/chart assets
- Docker configuration for local deployment

## Results / 当前结果

| Model | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: |
| Random Forest | 0.3331 | 0.5078 | 0.8051 |
| Ridge Regression | 0.5297 | 0.7356 | 0.5911 |
| Linear Regression | 0.5297 | 0.7356 | 0.5911 |

Random Forest is selected because it provides a much stronger R2 score while remaining compact enough for local deployment after optimization.

## Application Features / 应用能力

- Manual feature input for house area records
- Median income unit selector:
  - 10k USD/year
  - USD/year
  - USD/month
  - RMB/year
  - RMB/month
- Automatic conversion into the model unit: `MedInc = 10k USD/year`
- Prediction output in:
  - raw model unit: `100k USD`
  - estimated USD
  - estimated RMB in `10k RMB`
- Model metrics panel
- Model comparison table
- Bilingual field dictionary
- Key driver ranking and importance share chart
- Downloads:
  - prediction CSV
  - transparent SVG prediction summary
  - transparent SVG feature importance bar chart
  - transparent SVG importance share donut chart

## Project Structure / 项目结构

```text
02-smarthouse-regression/
  app.py
  config.json
  Dockerfile
  requirements.txt
  config/
    field_descriptions.json
  data/
    california_housing.csv
    sample_houses.csv
  models/
    house_price_model.joblib
  outputs/
    metrics.json
    model_comparison.csv
    report.html
  src/
    data_loader.py
    preprocessing.py
    models.py
    evaluator.py
    model_comparison.py
    price_units.py
    reporter.py
    train.py
    predict.py
```

## Run Locally / 本地运行

Install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Train the model:

```powershell
.\.venv\Scripts\python.exe .\src\train.py
```

Start the Streamlit app:

```powershell
.\.venv\Scripts\streamlit.exe run .\app.py --server.port 8502
```

Open:

```text
http://localhost:8502
```

## Docker / 容器运行

```powershell
docker build -t smarthouse-regression .
docker run --rm -p 8502:8501 smarthouse-regression
```

The container listens on `8501` internally and maps to local port `8502` to avoid conflicts with other local ML demos.

## Known Limits / 已知限制

- Dataset is California Housing, not Chinese real estate data.
- RMB conversion uses a fixed showcase assumption, not real-time exchange rates.
- Feature importance uses Random Forest `feature_importances_`; SHAP-level explanations are not included.
- This is a local single-user application without database, authentication, or production monitoring.

## Resume Summary / 简历描述

Built SmartHouse Regression, a tabular regression prediction system with automated model comparison, optimized Random Forest persistence, bilingual field presentation, unit conversion, Streamlit inference UI, feature-importance explanation, downloadable SVG/CSV reports, and Docker deployment support.
