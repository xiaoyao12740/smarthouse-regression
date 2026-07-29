# 02 - SmartHouse Regression / Intelligent House Price Prediction

这是第二个正式学习项目：从“分类问题”进入“回归问题”。第一个项目回答“它是什么”，本项目回答“它是多少”。

This is the second portfolio project: moving from classification to regression. The first project answers "what is it"; this project answers "how much is it".

## 项目定位 / Project Positioning

SmartHouse Regression 是一个基于 California Housing 数据集的房价回归预测演示系统。它不声称预测真实中国房价，而是在美国公开教学数据基础上训练回归模型，并为中文读者提供人民币换算展示。

SmartHouse Regression is a house price regression demo based on the California Housing dataset. It does not claim to predict real Chinese house prices. It trains regression models on a public U.S. teaching dataset and provides RMB conversion for easier presentation to Chinese readers.

## 项目目标 / Goals

- 理解回归任务和分类任务的区别
- 使用房屋特征预测房价
- 对比线性模型和非线性模型
- 学习 MAE、RMSE、R2 等回归评价指标
- 形成可复用的机器学习工程结构
- 将训练好的模型包装成本地可交互 Web 应用

## 技术栈 / Tech Stack

- Python
- pandas / numpy
- scikit-learn
- matplotlib
- joblib
- Streamlit
- Docker

## 当前模型 / Models

- `linear_regression`
- `ridge`
- `random_forest`

默认使用 `random_forest`，可以在 `config.json` 中修改。

Default model is `random_forest`. You can change it in `config.json`.

当前版本会自动比较三个模型，并输出：

The current version automatically compares three models and exports:

```text
outputs/model_comparison.csv
```

## 项目结构 / Project Structure

```text
02-smarthouse-regression/
  config.json
  requirements.txt
  data/
    california_housing.csv
    sample_houses.csv
  models/
    house_price_model.joblib
  outputs/
    metrics.json
    predictions.csv
    new_predictions.csv
    predicted_vs_actual.png
    feature_importance.png
    report.html
  src/
    data_loader.py
    preprocessing.py
    models.py
    evaluator.py
    reporter.py
    train.py
    predict.py
```

## 运行训练 / Train

在 `ML-DL-Projects` 总目录运行：

Run from the `ML-DL-Projects` root folder:

```powershell
.\.venv\Scripts\python.exe .\02-smarthouse-regression\src\train.py
```

## 运行预测 / Predict

训练完成后，使用示例房屋数据预测：

After training, predict with the sample house records:

```powershell
.\.venv\Scripts\python.exe .\02-smarthouse-regression\src\predict.py
```

也可以指定自己的 CSV：

You can also pass your own CSV:

```powershell
.\.venv\Scripts\python.exe .\02-smarthouse-regression\src\predict.py --input path\to\houses.csv
```

## 本地网页 / Local Web App

训练完成后，可以启动 Streamlit 页面：

After training, start the Streamlit app:

```powershell
.\.venv\Scripts\streamlit.exe run .\02-smarthouse-regression\app.py
```

页面包含：

- 手动输入房屋区域特征
- 展示原始预测值：`十万美元 / 100k USD`
- 展示美元估算值
- 展示人民币估算值：按固定假设 `1 USD = 6.6 RMB`
- 展示当前模型指标和模型比较结果
- 展示字段中英文说明
- 展示随机森林特征重要性，提供轻量级预测解释

默认端口：

Default port:

```text
http://localhost:8501
```

## Docker 运行 / Docker Run

构建镜像：

Build image:

```powershell
docker build -t smarthouse-regression .
```

启动容器：

Run container:

```powershell
docker run --rm -p 8501:8501 smarthouse-regression
```

停止方式：

Stop with `Ctrl+C` in the running terminal. Because `--rm` is used, the container is removed automatically after stopping.

## 怎么看结果 / How To Read Results

- `MAE`：平均预测误差，越低越好。
- `RMSE`：会更重地惩罚大错误，越低越好。
- `R2`：模型解释能力，越接近 1 越好。
- `predicted_vs_actual.png`：点越靠近红线，预测越准确。
- `feature_importance.png`：展示随机森林认为最重要的房屋特征。

## 双语展示 / Bilingual Presentation

本项目保留原始字段名用于训练，例如 `MedInc`、`AveRooms`、`HouseAge`。同时通过 `config/field_descriptions.json` 给报告、图表和展示版 CSV 增加中文名称与中英文说明。

The project keeps original field names for training, such as `MedInc`, `AveRooms`, and `HouseAge`. For human-facing outputs, `config/field_descriptions.json` adds Chinese names and bilingual descriptions to reports, charts, and display CSV files.

这样做的好处是：

- 不破坏原始数据和模型代码。
- 中国读者可以直接看懂输出结果。
- 未来如果用户上传中文业务数据，只需要调整字段词典和配置。

Generated bilingual outputs:

- `outputs/predictions_bilingual.csv`
- `outputs/new_predictions_bilingual.csv`
- `outputs/report.html`

Price unit note:

- The original California Housing target uses `100,000 USD` as the unit.
- For Chinese readers, this project also displays prediction results in `万元人民币 / 10k RMB`.
- The conversion uses a fixed showcase assumption: `1 USD = 6.6 RMB`.
- This is only for project demonstration, not real-time exchange-rate calculation.

## Current Result / 当前结果

After optimizing Random Forest depth and enabling model compression:

- Best model: `random_forest`
- MAE: `0.3331`
- RMSE: `0.5078`
- R2: `0.8051`
- Model size: about `10.02 MB`

The previous unbounded Random Forest model was about `155.35 MB`. The optimized version is much smaller while keeping nearly the same R2 score.

优化前未限制树深度的随机森林模型约 `155.35 MB`。优化后模型约 `10.02 MB`，R2 基本保持稳定，更适合作品展示和后续部署。

## Model Comparison / 模型比较

| Model | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: |
| Random Forest | 0.3331 | 0.5078 | 0.8051 |
| Ridge Regression | 0.5297 | 0.7356 | 0.5911 |
| Linear Regression | 0.5297 | 0.7356 | 0.5911 |

当前选择 Random Forest，因为它在 R2 上明显优于两个线性模型，同时优化后模型体积约 10MB，适合本地展示和 Docker 部署。

Random Forest is selected because it has a clearly higher R2 score than the two linear models, while the optimized model size remains around 10MB, suitable for local demos and Docker deployment.

## Screenshots / 截图位置

当前版本的主要视觉输出：

Current visual outputs:

- `outputs/predicted_vs_actual.png`
- `outputs/feature_importance.png`
- `outputs/report.html`

Streamlit 页面可以本地启动后截图，建议截图页面包括：

Recommended screenshots after launching Streamlit:

- Prediction page / 房价预测页
- Model page / 模型信息页
- Field dictionary page / 字段说明页

## Known Limits / 已知限制

- 数据来自 California Housing，不代表中国真实房地产市场。
- 人民币换算使用固定展示汇率 `1 USD = 6.6 RMB`，不是实时汇率。
- 当前解释性使用 Random Forest feature importance，尚未引入 SHAP 等更细粒度解释工具。
- 当前版本是单机演示应用，没有数据库、用户系统或线上监控。

## 简历表达 / Resume Line

> 构建 SmartHouse Regression 智能房价预测系统，支持房屋 CSV 数据读取、缺失值处理、回归模型训练、模型持久化、预测输出和可视化评估，使用 MAE、RMSE、R2 衡量模型表现。

> Built SmartHouse Regression, an intelligent house price prediction system with CSV ingestion, missing-value handling, regression training, model persistence, prediction export, and visual evaluation using MAE, RMSE, and R2.
