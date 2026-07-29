# SmartHouse Regression

SmartHouse Regression is a lightweight machine learning application for tabular regression and house-price prediction demos. It turns the California Housing dataset into a complete local workflow: data preparation, model comparison, optimized model persistence, unit conversion, explainable prediction output, Streamlit inference, report export, and Docker deployment.

SmartHouse Regression 是一个面向表格回归和房价预测演示的轻量级机器学习应用。项目基于 California Housing 数据集，完整串联了数据准备、模型对比、模型压缩保存、单位换算、预测解释、Streamlit 交互推理、报告导出和 Docker 本地部署。

## Positioning

The project is designed as a portfolio-grade regression system rather than a single training script. It shows how a classical machine learning model can be packaged into a usable prediction product with clear inputs, transparent assumptions, reproducible outputs, and a deployable web interface.

本项目定位为一个可展示的回归预测系统，而不是单个训练脚本。它展示了如何把传统机器学习模型封装成一个可使用的预测产品：输入清晰、假设透明、输出可复现，并且可以通过网页界面部署和演示。

The dataset is California Housing, so the model does not claim to predict real Chinese housing prices. RMB values are only display conversions based on the fixed showcase assumption `1 USD = 6.6 RMB`.

数据集来源于 California Housing，因此项目不声称预测真实中国房价。人民币结果仅用于展示换算，固定假设为 `1 USD = 6.6 RMB`。

## Highlights

- Config-driven regression pipeline
- CSV data preparation and sample prediction data
- Median imputation and feature scaling
- Linear Regression, Ridge, and Random Forest comparison
- Optimized Random Forest model size: about `10.02 MB`
- Streamlit prediction interface
- Income unit conversion before inference
- Prediction display in raw model units, USD, and RMB
- Feature importance explanation with percentage shares
- Downloadable CSV and transparent SVG report/chart assets
- Docker configuration for local deployment

中文概览：

- 使用配置文件驱动回归训练流程
- 自动准备 CSV 数据和预测样本
- 包含中位数缺失值填充与特征标准化
- 对比 Linear Regression、Ridge、Random Forest 三类模型
- 优化后的 Random Forest 模型约 `10.02 MB`
- 提供 Streamlit 本地预测界面
- 推理前支持收入单位换算
- 预测结果同时展示模型原始单位、美元和人民币
- 提供特征重要性排序与占比解释
- 支持下载 CSV 结果和透明背景 SVG 图表
- 提供 Docker 本地部署配置

## Results

| Model | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: |
| Random Forest | 0.3331 | 0.5078 | 0.8051 |
| Ridge Regression | 0.5297 | 0.7356 | 0.5911 |
| Linear Regression | 0.5297 | 0.7356 | 0.5911 |

Random Forest is selected because it provides a much stronger R2 score while remaining compact enough for local deployment after optimization.

当前版本选择 Random Forest 作为默认模型，因为它在 R2 上明显优于线性模型，并且经过压缩后仍适合本地部署和作品集展示。

## Application Features

Users can manually enter regional housing features, select the income unit they are using, run prediction, inspect model metrics, compare candidate models, read field explanations, and export prediction reports.

用户可以手动输入区域房屋特征，选择收入单位，运行预测，查看模型指标，对比候选模型，阅读字段解释，并导出预测报告。

Supported income input units:

- `10k USD/year`
- `USD/year`
- `USD/month`
- `RMB/year`
- `RMB/month`

Prediction outputs:

- raw model unit: `100k USD`
- estimated USD
- estimated RMB in `10k RMB`
- key feature importance ranking
- importance share chart

预测输出包括：

- 模型原始单位：`十万美元`
- 估算美元价格
- 以 `万元人民币` 展示的估算结果
- 关键特征重要性排序
- 特征重要性占比图

## Project Structure

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

## Run Locally

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

中文说明：

- 先创建并安装 Python 依赖
- 运行训练脚本生成模型和输出文件
- 再启动 Streamlit 页面进行本地预测演示
- 本项目建议使用 `8502` 端口，便于和其他本地机器学习演示并行运行

## Docker

```powershell
docker build -t smarthouse-regression .
docker run --rm -p 8502:8501 smarthouse-regression
```

The container listens on `8501` internally and maps to local port `8502` to avoid conflicts with other local ML demos.

容器内部监听 `8501`，本地映射到 `8502`，这样可以避免和其他 Streamlit 示例项目端口冲突。

## Known Limits

- Dataset is California Housing, not Chinese real estate data.
- RMB conversion uses a fixed showcase assumption, not real-time exchange rates.
- Feature importance uses Random Forest `feature_importances_`; SHAP-level explanations are not included.
- This is a local single-user application without database, authentication, or production monitoring.

中文补充：

- 当前数据集不是中国房地产交易数据，因此结果只能用于机器学习流程演示。
- 人民币换算不是实时汇率，也不是金融或交易建议。
- 特征解释使用随机森林内置重要性，适合轻量展示，但不是完整因果解释。
- 项目以本地作品集演示为目标，暂未加入数据库、登录鉴权和生产级监控。

## Resume Summary

Built SmartHouse Regression, a tabular regression prediction system with automated model comparison, optimized Random Forest persistence, unit conversion, Streamlit inference UI, feature-importance explanation, downloadable SVG/CSV reports, and Docker deployment support.

简历描述：构建 SmartHouse Regression 表格回归预测系统，完成自动模型对比、Random Forest 模型压缩保存、单位换算、Streamlit 推理界面、特征重要性解释、SVG/CSV 报告导出和 Docker 部署支持。
