# Model Report

## Scope

SmartHouse Regression packages a tabular regression workflow around the California Housing dataset. The report documents the current modeling setup, evaluation results, unit assumptions, and deployment constraints.

SmartHouse Regression 围绕 California Housing 数据集构建表格回归流程。本文档记录当前模型设置、评估结果、单位假设和部署限制。

## Dataset

The model uses the California Housing dataset with `median_house_value` as the target column. The target is measured in `100k USD`.

模型使用 California Housing 数据集，目标列为 `median_house_value`，原始目标单位为 `100k USD`。

The dataset describes block-group-level housing and demographic features in California. It is suitable for demonstrating a regression pipeline, but it should not be interpreted as a Chinese real-estate valuation dataset.

该数据集描述的是加州街区组层面的住房与人口统计特征，适合用于展示回归建模流程，但不应被理解为中国房地产估值数据。

## Pipeline

- CSV data preparation
- Median imputation for missing numeric values
- Feature scaling
- Linear Regression, Ridge, and Random Forest training
- Model comparison by MAE, RMSE, and R2
- Best-model persistence with `joblib`
- Prediction export and report generation
- Streamlit inference interface

中文说明：

- 准备 CSV 数据
- 对数值缺失值进行中位数填充
- 执行特征标准化
- 训练 Linear Regression、Ridge 和 Random Forest
- 使用 MAE、RMSE 和 R2 对比模型
- 使用 `joblib` 保存最佳模型
- 导出预测结果并生成报告
- 提供 Streamlit 推理界面

## Evaluation

| Model | MAE | RMSE | R2 |
| --- | ---: | ---: | ---: |
| Random Forest | 0.3331 | 0.5078 | 0.8051 |
| Ridge Regression | 0.5297 | 0.7356 | 0.5911 |
| Linear Regression | 0.5297 | 0.7356 | 0.5911 |

Random Forest is used as the default model because it provides the strongest R2 in the current comparison while keeping the optimized model artifact compact enough for local deployment.

当前版本默认使用 Random Forest，因为它在模型对比中取得最高 R2，并且优化后的模型文件仍适合本地部署。

## Unit Assumptions

The model output follows the dataset unit: `100k USD`. The application additionally converts predictions into USD and `10k RMB` for presentation.

模型输出沿用数据集单位：`100k USD`。应用层额外将预测值换算为美元和 `万元人民币` 便于展示。

Fixed presentation assumption:

```text
1 USD = 6.6 RMB
```

This is a fixed display assumption, not a real-time exchange rate.

该换算仅为固定展示假设，不是实时汇率。

## Constraints

- The dataset does not represent the Chinese housing market.
- RMB conversion is for display only.
- Feature importance is based on Random Forest `feature_importances_`.
- The application is designed for local single-user demonstration, without authentication, database storage, or production monitoring.

中文说明：

- 数据集不代表中国房地产市场
- 人民币换算仅用于页面展示
- 特征重要性基于 Random Forest 的 `feature_importances_`
- 应用定位为本地单用户演示，未包含鉴权、数据库存储或生产监控
